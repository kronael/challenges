// Chase-Lev work-stealing deque, fixed-size (CAP large enough, no resize).
// Owner pushes/pops at `bottom` (LIFO); thieves steal from `top` (FIFO).
// The last-element race (bottom-top == 1) is the whole point: owner's seq_cst
// `bottom` store and thief's seq_cst `top` ops form a Dekker pattern, so exactly
// one side wins the decisive CAS. Stress: 1 owner, 4 thieves, every task once.
#define _POSIX_C_SOURCE 200809L  // pthread_barrier_* under -std=c11
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define NTASKS 1000000u
#define NTHIEVES 4
#define CAP (1u << 21)  // 2M slots: > NTASKS, so push never overruns the buffer

#define EMPTY UINT64_MAX  // sentinel: deque had nothing for us
#define ABORT (UINT64_MAX - 1)  // thief lost the CAS race, may retry

typedef struct {
    _Atomic long top;     // thieves CAS here (seq_cst)
    _Atomic long bottom;  // owner reads/writes here
    uint64_t buf[CAP];
} Deque;

static void push(Deque *d, uint64_t task) {
    long b = atomic_load_explicit(&d->bottom, memory_order_relaxed);
    d->buf[b % CAP] = task;
    atomic_store_explicit(&d->bottom, b + 1, memory_order_release);
}

// Owner-only. Returns task, or EMPTY.
static uint64_t pop(Deque *d) {
    long b = atomic_load_explicit(&d->bottom, memory_order_relaxed) - 1;
    atomic_store_explicit(&d->bottom, b, memory_order_seq_cst);  // Dekker store
    long t = atomic_load_explicit(&d->top, memory_order_seq_cst);
    if (b < t) {  // deque was already empty
        atomic_store_explicit(&d->bottom, t, memory_order_relaxed);
        return EMPTY;
    }
    uint64_t val = d->buf[b % CAP];
    if (b > t) return val;  // >1 element, no thief can touch this one
    // b == t: last element. Race the thieves for it.
    uint64_t res = val;
    if (!atomic_compare_exchange_strong_explicit(&d->top, &t, t + 1,
                                                 memory_order_seq_cst, memory_order_seq_cst)) {
        res = EMPTY;  // a thief took it first
    }
    atomic_store_explicit(&d->bottom, t + 1, memory_order_relaxed);  // reset to empty
    return res;
}

// Any thief. Returns task, EMPTY (nothing there), or ABORT (lost the race).
static uint64_t steal(Deque *d) {
    long t = atomic_load_explicit(&d->top, memory_order_acquire);
    atomic_thread_fence(memory_order_seq_cst);  // Dekker fence vs owner's bottom store
    long b = atomic_load_explicit(&d->bottom, memory_order_acquire);
    if (t >= b) return EMPTY;
    uint64_t val = d->buf[t % CAP];
    if (atomic_compare_exchange_strong_explicit(&d->top, &t, t + 1,
                                               memory_order_seq_cst, memory_order_seq_cst)) {
        return val;
    }
    return ABORT;
}

static Deque deque;
static _Atomic uint64_t claimed[NTASKS];  // claimed[v] = how many times task v was taken
static _Atomic int owner_done = 0;
static pthread_barrier_t start;

static void claim(uint64_t v) {
    atomic_fetch_add_explicit(&claimed[v], 1, memory_order_relaxed);
}

static void *owner_fn(void *arg) {
    (void)arg;
    pthread_barrier_wait(&start);
    for (uint64_t i = 0; i < NTASKS; i++) push(&deque, i);
    // Owner drains its own end while thieves work the other end.
    for (;;) {
        uint64_t v = pop(&deque);
        if (v == EMPTY) {
            // Confirm truly empty: bottom <= top means nothing left for anyone.
            long b = atomic_load_explicit(&deque.bottom, memory_order_seq_cst);
            long t = atomic_load_explicit(&deque.top, memory_order_seq_cst);
            if (b <= t) break;
            continue;
        }
        claim(v);
    }
    atomic_store_explicit(&owner_done, 1, memory_order_release);
    return NULL;
}

static void *thief_fn(void *arg) {
    (void)arg;
    pthread_barrier_wait(&start);
    for (;;) {
        uint64_t v = steal(&deque);
        if (v == ABORT) continue;  // retry immediately
        if (v == EMPTY) {
            if (atomic_load_explicit(&owner_done, memory_order_acquire)) break;
            continue;  // owner may still push more (it doesn't here, but be honest)
        }
        claim(v);
    }
    return NULL;
}

int main(void) {
    atomic_store_explicit(&deque.top, 0, memory_order_relaxed);
    atomic_store_explicit(&deque.bottom, 0, memory_order_relaxed);

    pthread_t owner;
    pthread_t thieves[NTHIEVES];
    pthread_barrier_init(&start, NULL, NTHIEVES + 1);

    pthread_create(&owner, NULL, owner_fn, NULL);
    for (int i = 0; i < NTHIEVES; i++) pthread_create(&thieves[i], NULL, thief_fn, NULL);

    pthread_join(owner, NULL);
    for (int i = 0; i < NTHIEVES; i++) pthread_join(thieves[i], NULL);

    for (uint64_t i = 0; i < NTASKS; i++) {
        uint64_t c = atomic_load_explicit(&claimed[i], memory_order_relaxed);
        if (c != 1) {
            fprintf(stderr, "FAIL: task %llu claimed %llu times (expected 1)\n",
                    (unsigned long long)i, (unsigned long long)c);
            return 1;
        }
    }

    pthread_barrier_destroy(&start);
    printf("PASS\n");
    return 0;
}
