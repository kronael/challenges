// Sense-reversing reusable barrier for N threads, atomics only.
// The last arriver resets the count and flips the shared sense; everyone else
// spins on the flipped bit, not the count — so a stale count from phase K can
// never release a thread that has looped into phase K+1.
#define _POSIX_C_SOURCE 200112L
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>

#define N 8
#define PHASES 10000

static _Atomic int count = 0;
static _Atomic int sense = 0;

// Per-phase scratch: each thread writes the current phase, then after the
// barrier every thread asserts all N entries equal that phase.
static _Atomic int phase_results[N];
static _Atomic long violations = 0;

// local_sense is the thread's private bit; pass it in/out by pointer.
static void arrive_and_wait(int *local_sense) {
    *local_sense = !*local_sense;
    if (atomic_fetch_add_explicit(&count, 1, memory_order_acq_rel) == N - 1) {
        atomic_store_explicit(&count, 0, memory_order_relaxed);
        atomic_store_explicit(&sense, *local_sense, memory_order_release);  // release waiters
    } else {
        while (atomic_load_explicit(&sense, memory_order_acquire) != *local_sense) {
            /* spin */
        }
    }
}

typedef struct {
    int tid;
} Args;

static void *worker(void *p) {
    int tid = ((Args *)p)->tid;
    // Start at 0 so the first flip yields 1, which differs from the initial
    // shared sense=0 — otherwise phase-0 waiters fall straight through.
    int local_sense = 0;
    for (int phase = 0; phase < PHASES; phase++) {
        atomic_store_explicit(&phase_results[tid], phase, memory_order_relaxed);
        arrive_and_wait(&local_sense);
        // All threads are now in `phase`; nobody may have run ahead.
        for (int i = 0; i < N; i++) {
            if (atomic_load_explicit(&phase_results[i], memory_order_relaxed) != phase) {
                atomic_fetch_add_explicit(&violations, 1, memory_order_relaxed);
            }
        }
        // Second barrier so the post-check above completes before any thread
        // overwrites its slot for the next phase.
        arrive_and_wait(&local_sense);
    }
    return NULL;
}

int main(void) {
    pthread_t t[N];
    Args args[N];
    for (int i = 0; i < N; i++) atomic_store_explicit(&phase_results[i], -1, memory_order_relaxed);

    for (int i = 0; i < N; i++) {
        args[i].tid = i;
        pthread_create(&t[i], NULL, worker, &args[i]);
    }
    for (int i = 0; i < N; i++) pthread_join(t[i], NULL);

    long v = atomic_load_explicit(&violations, memory_order_relaxed);
    if (v != 0) {
        fprintf(stderr, "FAIL: %ld barrier violations (a thread ran ahead)\n", v);
        return 1;
    }
    printf("PASS\n");
    return 0;
}
