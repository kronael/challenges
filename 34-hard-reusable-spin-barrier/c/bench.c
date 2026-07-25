// Throughput: how fast N threads can cycle through the barrier.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 8
#define ROUNDS 200000

static SpinBarrier barrier;

static void *worker(void *p) {
	(void)p;
	int local_sense = 0;
	for (long round = 0; round < ROUNDS; round++) {
		barrier_wait(&barrier, &local_sense);
	}
	return NULL;
}

static double now_seconds(void) {
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

int main(void) {
	barrier_init(&barrier, N);

	pthread_t threads[N];
	double t0 = now_seconds();
	for (int i = 0; i < N; i++) {
		pthread_create(&threads[i], NULL, worker, NULL);
	}
	for (int i = 0; i < N; i++) {
		pthread_join(threads[i], NULL);
	}
	double elapsed = now_seconds() - t0;

	printf("barrier: %d threads, %d rounds in %.3fs\n", N, ROUNDS, elapsed);
	printf("barrier: %.0f ns per round\n", elapsed / ROUNDS * 1e9);
	return 0;
}
