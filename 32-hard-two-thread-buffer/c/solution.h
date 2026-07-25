#ifndef SOLUTION_H
#define SOLUTION_H

#include <stdatomic.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct {
	_Atomic size_t head;
	_Atomic size_t tail;
	uint64_t *buf;
	size_t cap;
} SpscQueue;

// cap must be a power of two.
void spsc_init(SpscQueue *q, size_t cap);
void spsc_destroy(SpscQueue *q);

// Producer thread only. Returns false when the buffer is full.
bool spsc_push(SpscQueue *q, uint64_t value);

// Consumer thread only. Returns false when the buffer is empty.
bool spsc_pop(SpscQueue *q, uint64_t *out);

#endif
