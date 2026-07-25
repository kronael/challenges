#include "solution.h"

#include <stdio.h>
#include <stdlib.h>

// High bits that no task value can reach, so a node read after it was released
// carries an obviously bogus payload instead of plausible data.
#define POISON 0xDEAD000000000000ull

static _Atomic uint64_t allocs = 0;
static _Atomic uint64_t frees = 0;

Node *node_alloc(uint64_t value) {
	Node *n = (Node *)malloc(sizeof *n);
	if (n == NULL) {
		perror("malloc");
		exit(1);
	}
	n->value = value;
	atomic_store_explicit(&n->next, NULL, memory_order_relaxed);
	atomic_fetch_add_explicit(&allocs, 1, memory_order_relaxed);
	return n;
}

void node_free(Node *n) {
	if (n == NULL) {
		return;
	}
	if (n->value >= POISON) {
		fprintf(stderr, "node freed twice\n");
		abort();
	}
	n->value = POISON;
	atomic_fetch_add_explicit(&frees, 1, memory_order_relaxed);
	free(n);
}

uint64_t node_allocs(void) {
	return atomic_load_explicit(&allocs, memory_order_relaxed);
}

uint64_t node_frees(void) {
	return atomic_load_explicit(&frees, memory_order_relaxed);
}

void stack_init(Stack *s) {
	atomic_store_explicit(&s->head, NULL, memory_order_relaxed);
}

void stack_destroy(Stack *s) {
	(void)s;
	fprintf(stderr, "stack_destroy: not implemented\n");
	abort();
}

void stack_push(Stack *s, uint64_t value) {
	(void)s;
	(void)value;
	fprintf(stderr, "stack_push: not implemented\n");
	abort();
}

bool stack_pop(Stack *s, uint64_t *out) {
	(void)s;
	(void)out;
	fprintf(stderr, "stack_pop: not implemented\n");
	abort();
}
