#ifndef SOLUTION_H
#define SOLUTION_H

#include <stdatomic.h>
#include <stdint.h>

typedef enum { POP_ITEM, POP_EMPTY, POP_RETRY } PopStatus;

typedef struct Node {
	_Atomic(struct Node *) next;
	uint64_t value;
} Node;

typedef struct {
	_Atomic(Node *) head;
	char pad[56];
	Node *tail;
} MpscQueue;

// Allocates the initial sentinel. Call once, before any producer starts.
void mpsc_init(MpscQueue *q);

// Releases every node the queue still owns. No thread may touch q afterwards.
void mpsc_destroy(MpscQueue *q);

// Callable from any number of threads simultaneously.
void mpsc_push(MpscQueue *q, uint64_t value);

// Callable from exactly one thread. On POP_ITEM the value is stored in *out;
// POP_RETRY means a producer is mid-enqueue and the caller should try again.
PopStatus mpsc_try_pop(MpscQueue *q, uint64_t *out);

#endif
