// Vyukov intrusive MPSC queue: wait-free push, single-consumer 3-valued try_pop.
// Reference: https://www.1024cores.net/home/lock-free-algorithms/queues/intrusive-mpsc-node-based-queue

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

// Heap-allocate the initial sentinel so the consumer can free reclaimed
// sentinels uniformly (no special case for the original stub).
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

// Wait-free: swap node into head, then publish the back-link. No CAS loop.
static void q_push(Queue *q, Node *node) {
	atomic_store_explicit(&node->next, NULL, memory_order_relaxed);
	Node *prev = atomic_exchange_explicit(&q->head, node, memory_order_acq_rel);
	atomic_store_explicit(&prev->next, node, memory_order_release);
}

typedef enum { GOT, EMPTY, RETRY } PopStatus;

// Single-consumer only. tail is the current sentinel; its successor carries the
// value and becomes the new sentinel.
static PopStatus q_try_pop(Queue *q, uint32_t *out, Node **freed) {
	Node *tail = q->tail;
	Node *next = atomic_load_explicit(&tail->next, memory_order_acquire);
	if (next != NULL) {
		q->tail = next;
		*out = next->val;
		*freed = tail;  // old sentinel is now consumer-owned, safe to reclaim
		return GOT;
	}
	Node *head = atomic_load_explicit(&q->head, memory_order_acquire);
	if (tail == head) {
		return EMPTY;
	}
	return RETRY;  // producer did the exchange but hasn't published next yet
}

static Queue queue;
static uint8_t seen[TOTAL];  // bitset would do; one byte each keeps it simple

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

// Decode (thread_id << 20) | seq into a dense [0, TOTAL) index.
static size_t index_of(uint32_t val) {
	uint32_t id = val >> 20;
	uint32_t seq = val & ((1u << 20) - 1);
	return (size_t)id * PER_PRODUCER + seq;
}

static void *consumer(void *arg) {
	_Atomic int *done = arg;
	long got = 0;
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
			got++;
		} else if (st == RETRY) {
			continue;  // producer mid-link; spin
		} else {  // EMPTY
			if (atomic_load_explicit(done, memory_order_acquire) && got == TOTAL) {
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
