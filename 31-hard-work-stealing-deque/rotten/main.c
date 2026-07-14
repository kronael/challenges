// ROTTEN: the owner takes the last element without competing with thieves on
// top. Stress pauses both sides after their stale observations so both claim
// the same task. A single-thread owner run remains correct.

#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define EMPTY UINT64_MAX

typedef struct {
    _Atomic long top;
    _Atomic long bottom;
    uint64_t slot;
} Deque;

static Deque deque;
static _Atomic int hook;
static _Atomic int owner_stage;
static _Atomic int thief_stage;

static void push(uint64_t value) {
    long bottom = atomic_load_explicit(&deque.bottom, memory_order_relaxed);
    deque.slot = value;
    atomic_store_explicit(&deque.bottom, bottom + 1, memory_order_release);
}

static uint64_t pop(void) {
    long bottom = atomic_load_explicit(&deque.bottom, memory_order_relaxed) - 1;
    atomic_store_explicit(&deque.bottom, bottom, memory_order_release);
    long top = atomic_load_explicit(&deque.top, memory_order_acquire);
    if (atomic_load_explicit(&hook, memory_order_relaxed)) {
        atomic_store_explicit(&owner_stage, 1, memory_order_release);
        while (atomic_load_explicit(&owner_stage, memory_order_acquire) != 2) {
        }
    }
    if (bottom < top) return EMPTY;
    // Naive: the owner assumes the final slot is its own. Correct with no thief,
    // but without a top CAS both sides can claim the last element.
    return deque.slot;
}

static uint64_t steal(void) {
    long top = atomic_load_explicit(&deque.top, memory_order_acquire);
    long bottom = atomic_load_explicit(&deque.bottom, memory_order_acquire);
    if (atomic_load_explicit(&hook, memory_order_relaxed)) {
        atomic_store_explicit(&thief_stage, 1, memory_order_release);
        while (atomic_load_explicit(&thief_stage, memory_order_acquire) != 2) {
        }
    }
    if (top >= bottom) return EMPTY;
    uint64_t value = deque.slot;
    if (!atomic_compare_exchange_strong_explicit(&deque.top, &top, top + 1,
                                                 memory_order_relaxed,
                                                 memory_order_relaxed))
        return EMPTY;
    return value;
}

static void reset(void) {
    atomic_store_explicit(&deque.top, 0, memory_order_relaxed);
    atomic_store_explicit(&deque.bottom, 0, memory_order_relaxed);
    atomic_store_explicit(&hook, 0, memory_order_relaxed);
}

static int weak_sanity(void) {
    reset();
    push(42);
    if (pop() != 42) return 1;
    puts("PASS");
    return 0;
}

static void *owner(void *raw) {
    *(uint64_t *)raw = pop();
    return NULL;
}

static void *thief(void *raw) {
    *(uint64_t *)raw = steal();
    return NULL;
}

static int adversarial_stress(void) {
    reset();
    push(42);
    atomic_store_explicit(&hook, 1, memory_order_relaxed);

    uint64_t stolen = EMPTY;
    uint64_t popped = EMPTY;
    pthread_t thief_thread;
    pthread_t owner_thread;
    pthread_create(&thief_thread, NULL, thief, &stolen);
    while (atomic_load_explicit(&thief_stage, memory_order_acquire) != 1) {
    }
    pthread_create(&owner_thread, NULL, owner, &popped);
    while (atomic_load_explicit(&owner_stage, memory_order_acquire) != 1) {
    }
    atomic_store_explicit(&thief_stage, 2, memory_order_release);
    pthread_join(thief_thread, NULL);
    atomic_store_explicit(&owner_stage, 2, memory_order_release);
    pthread_join(owner_thread, NULL);

    if (stolen == 42 && popped == 42) {
        fputs("FAIL: owner and thief both claimed the final task\n", stderr);
        return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "stress") == 0) return adversarial_stress();
    return weak_sanity();
}
