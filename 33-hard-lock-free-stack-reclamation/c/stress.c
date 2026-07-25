// Half the threads pop before they push and half do the reverse, so a node is
// very likely to be released while a peer still holds a pointer into it. Node
// accounting closes the loop: fewer frees than allocations is a leak, a second
// free of the same node trips the poison check inside node_free.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define THREADS 16
#define OPS 10000u

static Stack stack;
static pthread_barrier_t start;
static _Atomic unsigned long long popped = 0;
static _Atomic int corrupt = 0;

typedef struct {
	int id;
} Args;

static void take(uint64_t value) {
	if (value >= (uint64_t)THREADS * OPS) {
		atomic_store_explicit(&corrupt, 1, memory_order_relaxed);
	}
}

static void *worker(void *p) {
	const Args *args = (const Args *)p;
	unsigned long long local = 0;
	bool pop_heavy = args->id % 2 == 0;

	pthread_barrier_wait(&start);
	for (uint64_t i = 0; i < OPS; i++) {
		uint64_t value;
		if (pop_heavy) {
			if (stack_pop(&stack, &value)) {
				take(value);
				local++;
			}
			stack_push(&stack, (uint64_t)args->id * OPS + i);
		} else {
			stack_push(&stack, (uint64_t)args->id * OPS + i);
			if (stack_pop(&stack, &value)) {
				take(value);
				local++;
			}
		}
	}
	atomic_fetch_add_explicit(&popped, local, memory_order_relaxed);
	return NULL;
}

int main(void) {
	stack_init(&stack);
	pthread_barrier_init(&start, NULL, THREADS);

	pthread_t threads[THREADS];
	Args args[THREADS];
	for (int i = 0; i < THREADS; i++) {
		args[i].id = i;
		if (pthread_create(&threads[i], NULL, worker, &args[i]) != 0) {
			perror("pthread_create");
			return 1;
		}
	}
	for (int i = 0; i < THREADS; i++) {
		pthread_join(threads[i], NULL);
	}
	pthread_barrier_destroy(&start);

	unsigned long long drained = 0;
	uint64_t value;
	while (stack_pop(&stack, &value)) {
		take(value);
		drained++;
	}

	if (atomic_load_explicit(&corrupt, memory_order_relaxed) != 0) {
		fprintf(stderr, "FAIL: a pop returned a value that was never pushed\n");
		return 1;
	}

	unsigned long long pushed = (unsigned long long)THREADS * OPS;
	unsigned long long total = atomic_load_explicit(&popped, memory_order_relaxed) + drained;
	if (total != pushed) {
		fprintf(stderr, "FAIL: popped %llu of %llu — nodes lost or duplicated\n", total,
			pushed);
		return 1;
	}

	stack_destroy(&stack);

	if (node_allocs() != pushed) {
		fprintf(stderr, "FAIL: %llu allocations for %llu pushes\n",
			(unsigned long long)node_allocs(), pushed);
		return 1;
	}
	if (node_frees() != node_allocs()) {
		fprintf(stderr, "FAIL: %llu of %llu nodes released — leak or double free\n",
			(unsigned long long)node_frees(), (unsigned long long)node_allocs());
		return 1;
	}

	printf("ok: %d threads x %u ops, every node accounted for\n", THREADS, OPS);
	return 0;
}
