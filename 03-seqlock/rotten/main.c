// WRONG ON PURPOSE — the obvious "just memcpy it" non-solution.
//
// What's wrong: there is no sequence counter and no fence. The writer overwrites
// the 64-byte payload with a plain memcpy and the reader copies it with a plain
// memcpy. Nothing detects that a write overlapped the read, so a reader can
// stitch together bytes from two different ticks (a torn read), and the
// concurrent unsynchronised access is itself a data race / UB.
//
// Why it looks fine: single-threaded, every read returns exactly what was last
// written, so a trivial sanity check passes. It only fails once a real writer
// runs alongside the readers — which is exactly what the stress test in main()
// below does. Expect "FAIL: N torn reads".
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

// volatile only so the naive reload is not optimised to a single hoisted load;
// it provides NO ordering and NO atomicity — the slots can still be observed
// half-updated. This is the unsynchronised shared payload, the wrong thing.
static volatile Tick data;

// BUG: plain slot-by-slot store, no seq bump, no release. A reader can observe
// the payload after only some slots have been overwritten.
static void write_tick(const Tick *src) {
    for (int i = 0; i < 8; i++) data.v[i] = src->v[i];
}

// BUG: plain slot-by-slot load, no seq check, no fence, no retry. Always claims
// success even while a write is in flight, so torn reads are handed straight back.
static int read_tick(Tick *dst) {
    for (int i = 0; i < 8; i++) dst->v[i] = data.v[i];
    return 1;
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
