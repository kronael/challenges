// ROTTEN: q_try_pop() treats a temporarily unlinked producer node as EMPTY.
// A one-thread push/pop is correct. The stress mode pauses a producer after its
// head exchange but before it links prev->next, deterministically exposing the
// missing RETRY result without relying on scheduler luck.

#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    _Atomic(struct Node *) next;
    uint32_t val;
} Node;

typedef struct {
    _Atomic(Node *) head;
    Node *tail;
} Queue;

typedef enum { GOT, EMPTY, RETRY } PopStatus;

static _Atomic int pause_mid_link;
static _Atomic int stage;

static void q_init(Queue *q) {
    Node *stub = calloc(1, sizeof(*stub));
    if (stub == NULL) exit(2);
    atomic_store_explicit(&q->head, stub, memory_order_relaxed);
    q->tail = stub;
}

static void q_push(Queue *q, Node *node) {
    atomic_store_explicit(&node->next, NULL, memory_order_relaxed);
    Node *prev = atomic_exchange_explicit(&q->head, node, memory_order_acq_rel);
    if (atomic_load_explicit(&pause_mid_link, memory_order_relaxed)) {
        atomic_store_explicit(&stage, 1, memory_order_release);
        while (atomic_load_explicit(&stage, memory_order_acquire) != 2) {
        }
    }
    atomic_store_explicit(&prev->next, node, memory_order_release);
}

static PopStatus q_try_pop(Queue *q, uint32_t *out, Node **freed) {
    Node *tail = q->tail;
    Node *next = atomic_load_explicit(&tail->next, memory_order_acquire);
    if (next != NULL) {
        q->tail = next;
        *out = next->val;
        *freed = tail;
        return GOT;
    }
    // Naive: null next is always called EMPTY. Correct without concurrency, but
    // a mid-link producer needs RETRY or the consumer can drop pending work.
    return EMPTY;
}

typedef struct {
    Queue *q;
    Node *node;
} PushArg;

static void *push_thread(void *raw) {
    PushArg *arg = raw;
    q_push(arg->q, arg->node);
    return NULL;
}

static int weak_sanity(void) {
    Queue q;
    Node node = {.val = 7};
    q_init(&q);
    q_push(&q, &node);
    uint32_t out = 0;
    Node *freed = NULL;
    int ok = q_try_pop(&q, &out, &freed) == GOT && out == 7;
    free(freed);
    if (!ok) return 1;
    puts("PASS");
    return 0;
}

static int adversarial_stress(void) {
    Queue q;
    Node node = {.val = 9};
    q_init(&q);
    atomic_store_explicit(&pause_mid_link, 1, memory_order_relaxed);
    atomic_store_explicit(&stage, 0, memory_order_relaxed);

    PushArg arg = {&q, &node};
    pthread_t producer;
    pthread_create(&producer, NULL, push_thread, &arg);
    while (atomic_load_explicit(&stage, memory_order_acquire) != 1) {
    }

    uint32_t out = 0;
    Node *freed = NULL;
    PopStatus observed = q_try_pop(&q, &out, &freed);
    atomic_store_explicit(&stage, 2, memory_order_release);
    pthread_join(producer, NULL);

    if (observed == EMPTY && atomic_load_explicit(&q.head, memory_order_acquire) != q.tail) {
        fputs("FAIL: pending mid-link node reported as EMPTY\n", stderr);
        free(q.tail);
        return 1;
    }
    free(q.tail);
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "stress") == 0) return adversarial_stress();
    return weak_sanity();
}
