#ifndef SOLUTION_H
#define SOLUTION_H

#include <stdatomic.h>
#include <stdbool.h>
#include <stdint.h>

#define TICK_BYTES 64

typedef struct {
	_Atomic uint64_t seq;
	unsigned char data[TICK_BYTES];
} Seqlock;

void seqlock_init(Seqlock *s);

// Publishes a TICK_BYTES payload. Exactly one writer thread.
void seqlock_write(Seqlock *s, const unsigned char *buf);

// Copies the payload into out (TICK_BYTES). Returns false when a concurrent
// write was detected; the caller retries.
bool seqlock_read(Seqlock *s, unsigned char *out);

#endif
