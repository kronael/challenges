// ROTTEN: a cumulative arrival count has no phase marker. It releases one
// crossing correctly; on reuse the stale count is already at N, so a lone fast
// participant passes the next phase before its peer arrives.

#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <string.h>

#define N 2

static _Atomic int count;

static void arrive_and_wait(void) {
    atomic_fetch_add_explicit(&count, 1, memory_order_acq_rel);
    // Naive: wait for a single lifetime count to reach N. Correct once, but
    // O(1) stale state releases every later phase immediately.
    while (atomic_load_explicit(&count, memory_order_acquire) < N) {
    }
}

static void *one_arrival(void *raw) {
    (void)raw;
    arrive_and_wait();
    return NULL;
}

static int cross_once(void) {
    pthread_t peer;
    pthread_create(&peer, NULL, one_arrival, NULL);
    arrive_and_wait();
    pthread_join(peer, NULL);
    return 0;
}

static int weak_sanity(void) {
    atomic_store_explicit(&count, 0, memory_order_relaxed);
    cross_once();
    puts("PASS");
    return 0;
}

static int adversarial_stress(void) {
    atomic_store_explicit(&count, 0, memory_order_relaxed);
    cross_once();
    arrive_and_wait();
    if (atomic_load_explicit(&count, memory_order_relaxed) == N + 1) {
        fputs("FAIL: one participant crossed a reused barrier alone\n", stderr);
        return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "stress") == 0) return adversarial_stress();
    return weak_sanity();
}
