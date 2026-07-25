#include "solution.h"

#include <stdio.h>
#include <stdlib.h>

void deque_init(Deque *d) {
	d->cap = DEQUE_CAPACITY;
	d->buf = (uint64_t *)calloc(d->cap, sizeof *d->buf);
	if (d->buf == NULL) {
		perror("calloc");
		exit(1);
	}
	atomic_store_explicit(&d->bottom, 0, memory_order_relaxed);
	atomic_store_explicit(&d->top, 0, memory_order_relaxed);
}

void deque_destroy(Deque *d) {
	free(d->buf);
	d->buf = NULL;
	d->cap = 0;
}

void deque_push(Deque *d, uint64_t value) {
	(void)d;
	(void)value;
	fprintf(stderr, "deque_push: not implemented\n");
	abort();
}

bool deque_pop(Deque *d, uint64_t *out) {
	(void)d;
	(void)out;
	fprintf(stderr, "deque_pop: not implemented\n");
	abort();
}

StealStatus deque_steal(Deque *d, uint64_t *out) {
	(void)d;
	(void)out;
	fprintf(stderr, "deque_steal: not implemented\n");
	abort();
}
