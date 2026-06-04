// ROTTEN: the obvious-but-wrong MPSC pop.
//
// WHAT IS WRONG: q_try_pop() collapses the three-valued result into two. When
// tail->next is null it always returns EMPTY, never RETRY. But null next does
// NOT mean empty: a producer that has already done the head exchange
// (atomic_exchange on q->head) but has not yet published prev->next is mid-link.
// In that window the new node IS the head yet is unreachable from the tail, so
// tail->next reads null even though a message is in flight.
//
// Single-threaded this never triggers: with no concurrent producer there is no
// half-finished link, so push-then-pop round-trips every value. Under many
// producers the consumer hits the broken-link window, sees EMPTY, and (once the
// producers have signalled done) takes that as "queue drained" and exits while
// messages are still pending. Those messages are lost forever and the final
// seen[] sweep fails.
//
// The fix is in golden/main.c: distinguish tail==head (truly EMPTY) from
// tail!=head with a null next (RETRY — spin).

#include <assert.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PRODUCERS 8
#define PER_PRODUCER 100000
#define TOTAL (PRODUCERS * PER_PRODUCER)

typedef struct Node {
	_Atomic(struct Node *) next;
	uint32_t val;
} Node;

typedef struct {
	_Atomic(Node *) head;  // newest node, written by producers
	Node *tail;            // oldest pending node, consumer-only
} Queue;

static void q_init(Queue *q) {
	Node *stub = malloc(sizeof(Node));
	if (stub == NULL) {
		perror("malloc");
		exit(1);
	}
	atomic_store_explicit(&stub->next, NULL, memory_order_relaxed);
	stub->val = 0;
	atomic_store_explicit(&q->head, stub, memory_order_relaxed);
	q->tail = stub;
}

static void q_push(Queue *q, Node *node) {
	atomic_store_explicit(&node->next, NULL, memory_order_relaxed);
	Node *prev = atomic_exchange_explicit(&q->head, node, memory_order_acq_rel);
	atomic_store_explicit(&prev->next, node, memory_order_release);
}

typedef enum { GOT, EMPTY, RETRY } PopStatus;

// BUG: returns EMPTY whenever tail->next is null, never RETRY. A producer that
// is between its head exchange and its next publish is treated as "queue empty".
static PopStatus q_try_pop(Queue *q, uint32_t *out, Node **freed) {
	Node *tail = q->tail;
	Node *next = atomic_load_explicit(&tail->next, memory_order_acquire);
	if (next != NULL) {
		q->tail = next;
		*out = next->val;
		*freed = tail;
		return GOT;
	}
	return EMPTY;  // WRONG: a mid-link producer makes this look empty
}

static Queue queue;
static uint8_t seen[TOTAL];

static void *producer(void *arg) {
	uintptr_t id = (uintptr_t)arg;
	for (uint32_t seq = 0; seq < PER_PRODUCER; seq++) {
		Node *n = malloc(sizeof(Node));
		if (n == NULL) {
			perror("malloc");
			exit(1);
		}
		n->val = ((uint32_t)id << 20) | seq;
		q_push(&queue, n);
	}
	return NULL;
}

static size_t index_of(uint32_t val) {
	uint32_t id = val >> 20;
	uint32_t seq = val & ((1u << 20) - 1);
	return (size_t)id * PER_PRODUCER + seq;
}

static void *consumer(void *arg) {
	_Atomic int *done = arg;
	for (;;) {
		uint32_t val;
		Node *freed = NULL;
		PopStatus st = q_try_pop(&queue, &val, &freed);
		if (st == GOT) {
			size_t idx = index_of(val);
			assert(idx < TOTAL);
			assert(seen[idx] == 0 && "duplicate item");
			seen[idx] = 1;
			free(freed);
		} else if (st == RETRY) {
			continue;  // unreachable: this rotten pop never returns RETRY
		} else {  // EMPTY
			// Wrong shutdown: "producers finished and the queue looks empty, so
			// we're done." But EMPTY here can be a mid-link node, so we exit with
			// messages still pending and those messages are lost.
			if (atomic_load_explicit(done, memory_order_acquire)) {
				break;
			}
		}
	}
	return NULL;
}

int main(void) {
	q_init(&queue);
	memset(seen, 0, sizeof(seen));

	_Atomic int done = 0;
	pthread_t cons;
	pthread_create(&cons, NULL, consumer, &done);

	pthread_t prod[PRODUCERS];
	for (uintptr_t i = 0; i < PRODUCERS; i++) {
		pthread_create(&prod[i], NULL, producer, (void *)i);
	}
	for (int i = 0; i < PRODUCERS; i++) {
		pthread_join(prod[i], NULL);
	}
	atomic_store_explicit(&done, 1, memory_order_release);
	pthread_join(cons, NULL);

	for (size_t i = 0; i < TOTAL; i++) {
		if (seen[i] != 1) {
			fprintf(stderr, "FAIL: item %zu seen %d times\n", i, seen[i]);
			return 1;
		}
	}
	printf("PASS\n");
	return 0;
}
