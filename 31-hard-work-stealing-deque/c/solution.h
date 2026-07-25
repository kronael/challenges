#ifndef SOLUTION_H
#define SOLUTION_H

#include <stdatomic.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define DEQUE_CAPACITY (1u << 21)

typedef enum { STEAL_SUCCESS, STEAL_EMPTY, STEAL_RETRY } StealStatus;

typedef struct {
	_Atomic int64_t bottom;
	_Atomic int64_t top;
	uint64_t *buf;
	size_t cap;
} Deque;

// Allocates DEQUE_CAPACITY slots; the tests stay within that capacity.
void deque_init(Deque *d);
void deque_destroy(Deque *d);

// Owner thread only.
void deque_push(Deque *d, uint64_t value);

// Owner thread only. Returns false when the deque is empty.
bool deque_pop(Deque *d, uint64_t *out);

// Any number of thief threads. STEAL_RETRY means the caller lost a race and may
// try again; STEAL_EMPTY means the deque held nothing.
StealStatus deque_steal(Deque *d, uint64_t *out);

#endif
