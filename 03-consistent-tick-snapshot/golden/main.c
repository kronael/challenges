// Seqlock guarding a 64-byte tick (8 doubles): 1 writer, 8 wait-free readers.
// Writer bumps an odd/even seq around the payload copy; readers retry on
// odd-or-changed seq. The trailing acquire fence stops the CPU hoisting the
// payload load out of the guarded window (TSO hides this on x86, ARM exposes it).
#define _POSIX_C_SOURCE 200112L  // expose pthread_barrier_* under -std=c11
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define READERS 8
#define READER_ITERS 2000000u

typedef struct {
    double v[8];
} Tick;

static _Atomic uint64_t seq = 0;
static Tick data;

static void write_tick(const Tick *src) {
    atomic_fetch_add_explicit(&seq, 1, memory_order_release);  // seq -> odd
    memcpy(&data, src, sizeof(Tick));
    atomic_fetch_add_explicit(&seq, 1, memory_order_release);  // seq -> even
}

// Returns 1 on a clean read into *dst, 0 if the window was contended (retry).
static int read_tick(Tick *dst) {
    uint64_t s1 = atomic_load_explicit(&seq, memory_order_acquire);
    if (s1 & 1) return 0;
    memcpy(dst, &data, sizeof(Tick));
    atomic_thread_fence(memory_order_acquire);
    uint64_t s2 = atomic_load_explicit(&seq, memory_order_relaxed);
    return s2 == s1;
}

static _Atomic int stop = 0;
static _Atomic uint64_t written = 0;       // writer's last counter, for progress check
static _Atomic uint64_t torn = 0;          // count of inconsistent (torn) reads
static _Atomic uint64_t max_seen = 0;      // highest consistent value any reader saw
static pthread_barrier_t start;

static void *writer_fn(void *arg) {
    (void)arg;
    pthread_barrier_wait(&start);
    uint64_t counter = 1;
    Tick t;
    while (!atomic_load_explicit(&stop, memory_order_relaxed)) {
        for (int i = 0; i < 8; i++) t.v[i] = (double)counter;
        write_tick(&t);
        counter++;
    }
    atomic_store_explicit(&written, counter, memory_order_relaxed);
    return NULL;
}

static void *reader_fn(void *arg) {
    (void)arg;
    Tick local;
    uint64_t local_max = 0;
    pthread_barrier_wait(&start);
    for (uint64_t i = 0; i < READER_ITERS; i++) {
        while (!read_tick(&local)) { /* spin */ }
        double first = local.v[0];
        int consistent = 1;
        for (int j = 1; j < 8; j++) {
            if (local.v[j] != first) { consistent = 0; break; }
        }
        if (consistent) {
            if ((uint64_t)first > local_max) local_max = (uint64_t)first;
        } else {
            atomic_fetch_add_explicit(&torn, 1, memory_order_relaxed);
        }
    }
    uint64_t cur = atomic_load_explicit(&max_seen, memory_order_relaxed);
    while (local_max > cur &&
           !atomic_compare_exchange_weak_explicit(&max_seen, &cur, local_max,
                                                  memory_order_relaxed, memory_order_relaxed)) {
    }
    return NULL;
}

int main(void) {
    pthread_t writer;
    pthread_t readers[READERS];
    pthread_barrier_init(&start, NULL, READERS + 1);

    pthread_create(&writer, NULL, writer_fn, NULL);
    for (int i = 0; i < READERS; i++) pthread_create(&readers[i], NULL, reader_fn, NULL);

    for (int i = 0; i < READERS; i++) pthread_join(readers[i], NULL);
    atomic_store_explicit(&stop, 1, memory_order_relaxed);
    pthread_join(writer, NULL);

    if (atomic_load_explicit(&torn, memory_order_relaxed) != 0) {
        fprintf(stderr, "FAIL: %llu torn reads\n",
                (unsigned long long)atomic_load_explicit(&torn, memory_order_relaxed));
        return 1;
    }
    // Sanity: the writer advanced and readers saw real, progressing values, so a
    // degenerate no-op impl cannot pass.
    if (atomic_load_explicit(&written, memory_order_relaxed) <= 1) {
        fprintf(stderr, "FAIL: writer never advanced the sequence\n");
        return 1;
    }
    if (atomic_load_explicit(&max_seen, memory_order_relaxed) == 0) {
        fprintf(stderr, "FAIL: readers never observed a written value\n");
        return 1;
    }

    pthread_barrier_destroy(&start);
    printf("PASS\n");
    return 0;
}
