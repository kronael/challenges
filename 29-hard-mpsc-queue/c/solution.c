#include "solution.h"

#include <stdio.h>
#include <stdlib.h>

static Node *node_new(uint64_t value) {
	Node *n = (Node *)malloc(sizeof *n);
	if (n == NULL) {
		perror("malloc");
		exit(1);
	}
	atomic_store_explicit(&n->next, NULL, memory_order_relaxed);
	n->value = value;
	return n;
}

void mpsc_init(MpscQueue *q) {
	Node *stub = node_new(0);
	atomic_store_explicit(&q->head, stub, memory_order_relaxed);
	q->tail = stub;
}

void mpsc_destroy(MpscQueue *q) {
	Node *n = q->tail;
	while (n != NULL) {
		Node *next = atomic_load_explicit(&n->next, memory_order_relaxed);
		free(n);
		n = next;
	}
	q->tail = NULL;
	atomic_store_explicit(&q->head, NULL, memory_order_relaxed);
}

void mpsc_push(MpscQueue *q, uint64_t value) {
	(void)q;
	(void)value;
	fprintf(stderr, "mpsc_push: not implemented\n");
	abort();
}

PopStatus mpsc_try_pop(MpscQueue *q, uint64_t *out) {
	(void)q;
	(void)out;
	fprintf(stderr, "mpsc_try_pop: not implemented\n");
	abort();
}
