#include "solution.h"

#include <stdio.h>
#include <stdlib.h>

void spsc_init(SpscQueue *q, size_t cap) {
	if (cap == 0 || (cap & (cap - 1)) != 0) {
		fprintf(stderr, "capacity must be a power of two\n");
		exit(1);
	}
	q->buf = (uint64_t *)calloc(cap, sizeof *q->buf);
	if (q->buf == NULL) {
		perror("calloc");
		exit(1);
	}
	q->cap = cap;
	atomic_store_explicit(&q->head, 0, memory_order_relaxed);
	atomic_store_explicit(&q->tail, 0, memory_order_relaxed);
}

void spsc_destroy(SpscQueue *q) {
	free(q->buf);
	q->buf = NULL;
	q->cap = 0;
}

bool spsc_push(SpscQueue *q, uint64_t value) {
	(void)q;
	(void)value;
	fprintf(stderr, "spsc_push: not implemented\n");
	abort();
}

bool spsc_pop(SpscQueue *q, uint64_t *out) {
	(void)q;
	(void)out;
	fprintf(stderr, "spsc_pop: not implemented\n");
	abort();
}
