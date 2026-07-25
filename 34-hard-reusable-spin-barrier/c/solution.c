#include "solution.h"

#include <stdio.h>
#include <stdlib.h>

void barrier_init(SpinBarrier *b, int n) {
	if (n <= 0) {
		fprintf(stderr, "barrier size must be positive\n");
		exit(1);
	}
	b->n = n;
	atomic_store_explicit(&b->count, n, memory_order_relaxed);
	atomic_store_explicit(&b->sense, 0, memory_order_relaxed);
}

void barrier_wait(SpinBarrier *b, int *local_sense) {
	(void)b;
	(void)local_sense;
	fprintf(stderr, "barrier_wait: not implemented\n");
	abort();
}
