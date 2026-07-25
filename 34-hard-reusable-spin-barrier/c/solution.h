#ifndef SOLUTION_H
#define SOLUTION_H

#include <stdatomic.h>

typedef struct {
	int n;
	_Atomic int count;
	_Atomic int sense;
} SpinBarrier;

// n must be positive. Call once, before any thread waits.
void barrier_init(SpinBarrier *b, int n);

// Blocks until all n participants have called it. Each thread keeps its own
// local_sense, initialised to 0 and owned by that thread across every round.
void barrier_wait(SpinBarrier *b, int *local_sense);

#endif
