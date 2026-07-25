// Throughput: PRODUCERS threads push, this thread drains.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define PRODUCERS 4
#define PER_PRODUCER 2000000ull

static MpscQueue queue;
static pthread_barrier_t start;

static void *producer_fn(void *arg) {
	(void)arg;
	pthread_barrier_wait(&start);
	for (uint64_t value = 0; value < PER_PRODUCER; value++) {
		mpsc_push(&queue, value);
	}
	return NULL;
}

static double now_seconds(void) {
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

int main(void) {
	mpsc_init(&queue);
	pthread_barrier_init(&start, NULL, PRODUCERS);

	pthread_t producers[PRODUCERS];
	for (int i = 0; i < PRODUCERS; i++) {
		pthread_create(&producers[i], NULL, producer_fn, NULL);
	}

	double t0 = now_seconds();
	unsigned long long total = PRODUCERS * PER_PRODUCER;
	unsigned long long popped = 0;
	uint64_t checksum = 0;
	while (popped < total) {
		uint64_t value;
		if (mpsc_try_pop(&queue, &value) == POP_ITEM) {
			checksum += value;
			popped++;
		}
	}
	double elapsed = now_seconds() - t0;

	for (int i = 0; i < PRODUCERS; i++) {
		pthread_join(producers[i], NULL);
	}
	pthread_barrier_destroy(&start);
	mpsc_destroy(&queue);

	printf("mpsc: %d producers, %llu msgs in %.3fs\n", PRODUCERS, total, elapsed);
	printf("mpsc: %.1f Mops/s consumed (checksum %llu)\n", (double)total / elapsed / 1e6,
	       (unsigned long long)checksum);
	return 0;
}
