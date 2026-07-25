#include "solution.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void seqlock_init(Seqlock *s) {
	atomic_store_explicit(&s->seq, 0, memory_order_relaxed);
	memset(s->data, 0, sizeof s->data);
}

void seqlock_write(Seqlock *s, const unsigned char *buf) {
	(void)s;
	(void)buf;
	fprintf(stderr, "seqlock_write: not implemented\n");
	abort();
}

bool seqlock_read(Seqlock *s, unsigned char *out) {
	(void)s;
	(void)out;
	fprintf(stderr, "seqlock_read: not implemented\n");
	abort();
}
