// ROTTEN: plain Treiber stack with NO hazard pointers. Popped nodes are recycled
// through a lock-free free-list instead of being protected before reuse. This is
// the obvious, tempting version: it is correct single-threaded and passes a quick
// one-thread sanity run, but under concurrency it ABA-corrupts and loses nodes.
//
// WHAT IS WRONG:
//   pop() loads head (= node A), loads A->next (= node B), then CASes head A -> B.
//   Between the load of A->next and the CAS, another thread can pop A, pop B,
//   recycle A, and push A back on top of some other node C. Our stale CAS swaps
//   head A -> B *succeeds* on the pointer value — but B was meanwhile recycled and
//   re-pushed elsewhere, so the stack now points into the wrong chain. The result:
//   a value popped twice, a value lost (popped zero times), or a thread spinning
//   forever waiting on a node that no longer exists. That is the ABA problem.
//
// The fix is to publish each node to a per-thread hazard slot and re-validate head
// before dereferencing, deferring reclamation until no slot guards the node (see
// golden/main.c). Single-thread runs never recycle under a live reader, so this
// file "works" until the stress test runs it from 8 threads.
#define _POSIX_C_SOURCE 200809L  // pthread_barrier_* under -std=c11
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define NTHREADS 8
#define PER_THREAD 10000u
#define NTASKS (NTHREADS * PER_THREAD)

typedef struct Node {
    _Atomic(struct Node *) next;
    uint64_t val;
} Node;

static _Atomic(Node *) stack_head = NULL;
static _Atomic(Node *) freelist = NULL;  // recycled nodes — the ABA accelerant

static _Atomic uint64_t allocs = 0;

// Lock-free free-list: this is where reclamation should have used hazard pointers.
static Node *fl_pop(void) {
    Node *h = atomic_load_explicit(&freelist, memory_order_acquire);
    while (h) {
        Node *nx = atomic_load_explicit(&h->next, memory_order_acquire);
        if (atomic_compare_exchange_weak_explicit(&freelist, &h, nx, memory_order_acq_rel,
                                                  memory_order_acquire))
            return h;
    }
    return NULL;
}

static void fl_push(Node *n) {
    Node *h = atomic_load_explicit(&freelist, memory_order_relaxed);
    do {
        atomic_store_explicit(&n->next, h, memory_order_relaxed);
    } while (!atomic_compare_exchange_weak_explicit(&freelist, &h, n, memory_order_release,
                                                    memory_order_relaxed));
}

static Node *get_node(uint64_t v) {
    Node *n = fl_pop();
    if (!n) {
        n = malloc(sizeof(Node));
        if (!n) {
            fprintf(stderr, "FAIL: malloc\n");
            exit(1);
        }
        atomic_fetch_add_explicit(&allocs, 1, memory_order_relaxed);
    }
    n->val = v;
    atomic_store_explicit(&n->next, NULL, memory_order_relaxed);
    return n;
}

static void push(uint64_t v) {
    Node *n = get_node(v);
    Node *h = atomic_load_explicit(&stack_head, memory_order_relaxed);
    do {
        atomic_store_explicit(&n->next, h, memory_order_relaxed);
    } while (!atomic_compare_exchange_weak_explicit(&stack_head, &h, n,
                                                    memory_order_release, memory_order_relaxed));
}

// Returns 1 and writes *out on success, 0 if the stack was empty.
// BUG: dereferences h and CASes on its raw pointer value with no hazard pointer,
// then recycles h — a peer's in-flight pop can ABA-corrupt the chain.
static int pop(uint64_t *out) {
    for (;;) {
        Node *h = atomic_load_explicit(&stack_head, memory_order_acquire);
        if (!h) return 0;
        Node *next = atomic_load_explicit(&h->next, memory_order_acquire);
        if (atomic_compare_exchange_strong_explicit(&stack_head, &h, next,
                                                    memory_order_seq_cst, memory_order_relaxed)) {
            *out = h->val;
            fl_push(h);  // BUG: recycled with no hazard check — fuels ABA
            return 1;
        }
    }
}

static _Atomic uint64_t claimed[NTASKS];  // claimed[v]++ on each pop
static pthread_barrier_t phase;

typedef struct {
    int tid;
} Arg;

static void take(uint64_t v) {
    if (v >= NTASKS) {
        fprintf(stderr, "FAIL: popped oob value %llu\n", (unsigned long long)v);
        exit(1);
    }
    atomic_fetch_add_explicit(&claimed[v], 1, memory_order_relaxed);
}

static void *worker(void *p) {
    int tid = ((Arg *)p)->tid;
    uint64_t base = (uint64_t)tid * PER_THREAD;

    pthread_barrier_wait(&phase);

    for (uint64_t i = 0; i < PER_THREAD; i++) push(base + i);
    for (uint64_t i = 0; i < PER_THREAD; i++) {
        uint64_t v;
        while (!pop(&v)) { /* spin: another thread is mid-update */ }
        take(v);
    }
    return NULL;
}

int main(void) {
    pthread_t th[NTHREADS];
    Arg args[NTHREADS];
    pthread_barrier_init(&phase, NULL, NTHREADS);

    for (int i = 0; i < NTHREADS; i++) {
        args[i].tid = i;
        pthread_create(&th[i], NULL, worker, &args[i]);
    }
    for (int i = 0; i < NTHREADS; i++) pthread_join(th[i], NULL);

    if (atomic_load_explicit(&stack_head, memory_order_seq_cst) != NULL) {
        fprintf(stderr, "FAIL: stack not empty\n");
        return 1;
    }
    for (uint64_t i = 0; i < NTASKS; i++) {
        uint64_t c = atomic_load_explicit(&claimed[i], memory_order_relaxed);
        if (c != 1) {
            fprintf(stderr, "FAIL: value %llu popped %llu times (expected 1)\n",
                    (unsigned long long)i, (unsigned long long)c);
            return 1;
        }
    }

    pthread_barrier_destroy(&phase);
    printf("PASS\n");
    return 0;
}
