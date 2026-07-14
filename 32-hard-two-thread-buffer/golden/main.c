#include <pthread.h>
#include <stdatomic.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CAPACITY 1024  // power of 2
#define MASK (CAPACITY - 1)
#define N 10000000ULL

typedef struct {
    _Alignas(64) _Atomic uint64_t tail;  // producer writes
    _Alignas(64) _Atomic uint64_t head;  // consumer writes
    uint64_t slots[CAPACITY];
} RingBuf;

// push (producer only) — returns false if full
static bool push(RingBuf *rb, uint64_t val) {
    uint64_t t = atomic_load_explicit(&rb->tail, memory_order_relaxed);
    uint64_t h = atomic_load_explicit(&rb->head, memory_order_acquire);
    if (t - h == CAPACITY) return false;  // full
    rb->slots[t & MASK] = val;
    atomic_store_explicit(&rb->tail, t + 1, memory_order_release);
    return true;
}

// pop (consumer only) — returns false if empty
static bool pop(RingBuf *rb, uint64_t *out) {
    uint64_t h = atomic_load_explicit(&rb->head, memory_order_relaxed);
    uint64_t t = atomic_load_explicit(&rb->tail, memory_order_acquire);
    if (h == t) return false;  // empty
    *out = rb->slots[h & MASK];
    atomic_store_explicit(&rb->head, h + 1, memory_order_release);
    return true;
}

static void *producer(void *arg) {
    RingBuf *rb = arg;
    for (uint64_t i = 0; i < N; i++) {
        while (!push(rb, i)) {
            // spin on full
        }
    }
    return NULL;
}

static void *consumer(void *arg) {
    RingBuf *rb = arg;
    uint64_t expected = 0;
    uint64_t v;
    while (expected < N) {
        if (pop(rb, &v)) {
            if (v != expected) {
                fprintf(stderr, "FAIL: expected %llu got %llu\n",
                        (unsigned long long)expected, (unsigned long long)v);
                exit(1);
            }
            expected++;
        }
    }
    return NULL;
}

int main(void) {
    RingBuf *rb = calloc(1, sizeof(RingBuf));
    if (!rb) {
        perror("calloc");
        return 1;
    }
    atomic_store_explicit(&rb->tail, 0, memory_order_relaxed);
    atomic_store_explicit(&rb->head, 0, memory_order_relaxed);

    pthread_t pt, ct;
    pthread_create(&ct, NULL, consumer, rb);
    pthread_create(&pt, NULL, producer, rb);
    pthread_join(pt, NULL);
    pthread_join(ct, NULL);

    free(rb);
    printf("PASS\n");
    return 0;
}
