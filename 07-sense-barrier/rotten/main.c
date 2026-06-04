// WRONG ON PURPOSE — the obvious "increment a count, spin until count == N,
// then reset" barrier with NO sense reversal.
//
// What's wrong: there is one shared count and nothing that distinguishes
// phase K from phase K+1. The last arriver resets the count to 0, but a fast
// thread that has already left this phase and looped into the next one can
// observe the count == N condition (or a still-high count) before its peers
// from the previous phase have left, and sail straight through. There is no
// per-thread sense bit gating the release, so a stale count releases threads
// early. (As a bonus, the reset races the waiters' reads of the count.)
//
// Why it looks fine: with a single barrier crossing — every thread arrives once
// and is released once — the count reaches N exactly once and everyone leaves
// together, so a trivial one-shot sanity check passes. It only breaks once the
// same barrier is reused across many phases at speed, which is exactly what the
// stress loop in main() below does. Expect "FAIL: N barrier violations".
#define _POSIX_C_SOURCE 200112L
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>

#define N 8
#define PHASES 2000

static _Atomic int count = 0;

// Per-phase scratch: each thread writes the current phase, then after the
// barrier every thread asserts all N entries equal that phase.
static _Atomic int phase_results[N];
static _Atomic long violations = 0;

// BUG: no sense bit. Spin until the count reaches N, then the last arriver
// resets it to 0. Nothing distinguishes phase K from phase K+1: a fast thread
// that loops back and calls arrive_and_wait again can see the count still at N
// (the last arriver has not reset it yet) and be released immediately, before
// its peers from the previous phase have left — a stale count releasing a
// thread early. (The same missing phase bit also lets the naive barrier
// deadlock when the reset to 0 races the spinners; the bounded spin below caps
// that so the harness sees the early-release violations instead of hanging
// forever — either way it is broken.)
static void arrive_and_wait(void) {
    if (atomic_fetch_add_explicit(&count, 1, memory_order_acq_rel) == N - 1) {
        // last arriver: release everyone, then reset for the next round
        atomic_store_explicit(&count, 0, memory_order_release);
    } else {
        // everyone else spins until the count reaches N — the stale-count trap
        long spins = 0;
        while (atomic_load_explicit(&count, memory_order_acquire) < N) {
            if (++spins > 1000000L) break;  // give up so the test can terminate
        }
    }
}

typedef struct {
    int tid;
} Args;

static void *worker(void *p) {
    int tid = ((Args *)p)->tid;
    for (int phase = 0; phase < PHASES; phase++) {
        atomic_store_explicit(&phase_results[tid], phase, memory_order_relaxed);
        arrive_and_wait();
        // All threads should be in `phase`; nobody may have run ahead.
        for (int i = 0; i < N; i++) {
            if (atomic_load_explicit(&phase_results[i], memory_order_relaxed) != phase) {
                atomic_fetch_add_explicit(&violations, 1, memory_order_relaxed);
            }
        }
        // Second barrier so the post-check above completes before any thread
        // overwrites its slot for the next phase.
        arrive_and_wait();
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
