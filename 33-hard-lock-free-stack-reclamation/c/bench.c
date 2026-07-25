// Throughput: every thread alternates push and pop on the shared stack.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define THREADS 8
#define OPS 500000u

static Stack stack;
static pthread_barrier_t start;

typedef struct {
	int id;
} Args;

static void *worker(void *p) {
	const Args *args = (const Args *)p;
	pthread_barrier_wait(&start);
	for (uint64_t i = 0; i < OPS; i++) {
		uint64_t value;
		stack_push(&stack, (uint64_t)args->id * OPS + i);
		stack_pop(&stack, &value);
	}
	return NULL;
}

static double now_seconds(void) {
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

int main(void) {
	stack_init(&stack);
	pthread_barrier_init(&start, NULL, THREADS);

	pthread_t threads[THREADS];
	Args args[THREADS];
	double t0 = now_seconds();
	for (int i = 0; i < THREADS; i++) {
		args[i].id = i;
		pthread_create(&threads[i], NULL, worker, &args[i]);
	}
	for (int i = 0; i < THREADS; i++) {
		pthread_join(threads[i], NULL);
	}
	double elapsed = now_seconds() - t0;
	pthread_barrier_destroy(&start);
	stack_destroy(&stack);

	double ops = (double)THREADS * OPS * 2;
	printf("stack: %d threads, %.0f ops in %.3fs\n", THREADS, ops, elapsed);
	printf("stack: %.1f Mops/s\n", ops / elapsed / 1e6);
	return 0;
}
