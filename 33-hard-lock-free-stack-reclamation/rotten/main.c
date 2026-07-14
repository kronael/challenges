// ROTTEN: a pop dereferences a raw head pointer and immediately permits reuse.
// Stress pauses one pop after it reads A->B, removes A and B, reuses A, then
// resumes the stale CAS. The pointer value is A again, so the CAS resurrects B.

#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct Node {
    _Atomic(struct Node *) next;
    uint64_t value;
} Node;

static _Atomic(Node *) head;
static _Atomic int pause_pop;
static _Atomic int stage;

static void push_node(Node *node) {
    Node *old = atomic_load_explicit(&head, memory_order_relaxed);
    do {
        atomic_store_explicit(&node->next, old, memory_order_relaxed);
    } while (!atomic_compare_exchange_weak_explicit(&head, &old, node,
                                                    memory_order_release,
                                                    memory_order_relaxed));
}

static Node *pop_node(void) {
    Node *old = atomic_load_explicit(&head, memory_order_acquire);
    while (old != NULL) {
        Node *next = atomic_load_explicit(&old->next, memory_order_acquire);
        if (atomic_load_explicit(&pause_pop, memory_order_relaxed)) {
            atomic_store_explicit(&stage, 1, memory_order_release);
            while (atomic_load_explicit(&stage, memory_order_acquire) != 2) {
            }
        }
        // Naive: CAS a recyclable raw address with no hazard publication.
        // Correct alone, but reuse can make this stale address look current.
        if (atomic_compare_exchange_strong_explicit(&head, &old, next,
                                                    memory_order_seq_cst,
                                                    memory_order_relaxed))
            return old;
    }
    return NULL;
}

static int weak_sanity(void) {
    Node a = {.value = 1};
    Node b = {.value = 2};
    atomic_store_explicit(&head, NULL, memory_order_relaxed);
    push_node(&b);
    push_node(&a);
    if (pop_node() != &a || pop_node() != &b || pop_node() != NULL) return 1;
    puts("PASS");
    return 0;
}

static void *paused_pop(void *raw) {
    *(Node **)raw = pop_node();
    return NULL;
}

static int adversarial_stress(void) {
    Node a = {.value = 1};
    Node b = {.value = 2};
    Node c = {.value = 3};
    atomic_store_explicit(&head, NULL, memory_order_relaxed);
    push_node(&c);
    push_node(&b);
    push_node(&a);
    atomic_store_explicit(&pause_pop, 1, memory_order_relaxed);
    atomic_store_explicit(&stage, 0, memory_order_relaxed);

    Node *stale_result = NULL;
    pthread_t reader;
    pthread_create(&reader, NULL, paused_pop, &stale_result);
    while (atomic_load_explicit(&stage, memory_order_acquire) != 1) {
    }

    atomic_store_explicit(&pause_pop, 0, memory_order_relaxed);
    Node *first = pop_node();
    Node *second = pop_node();
    first->value = 99;
    push_node(first);
    atomic_store_explicit(&stage, 2, memory_order_release);
    pthread_join(reader, NULL);

    if (stale_result == &a && atomic_load_explicit(&head, memory_order_acquire) == second) {
        fputs("FAIL: stale CAS resurrected a reclaimed node (ABA)\n", stderr);
        return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "stress") == 0) return adversarial_stress();
    return weak_sanity();
}
