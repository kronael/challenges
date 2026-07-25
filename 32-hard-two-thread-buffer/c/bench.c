// Throughput: one producer, one consumer, no other traffic.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MESSAGES 20000000ull
#define CAP 4096

static SpscQueue queue;
static pthread_barrier_t start;

static void *producer_fn(void *arg) {
	(void)arg;
	pthread_barrier_wait(&start);
	for (uint64_t value = 0; value < MESSAGES; value++) {
		while (!spsc_push(&queue, value)) {
		}
	}
	return NULL;
}

static double now_seconds(void) {
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

int main(void) {
	spsc_init(&queue, CAP);
	pthread_barrier_init(&start, NULL, 2);

	pthread_t producer;
	pthread_create(&producer, NULL, producer_fn, NULL);

	pthread_barrier_wait(&start);
	double t0 = now_seconds();
	uint64_t checksum = 0;
	for (uint64_t received = 0; received < MESSAGES; received++) {
		uint64_t value;
		while (!spsc_pop(&queue, &value)) {
		}
		checksum += value;
	}
	double elapsed = now_seconds() - t0;

	pthread_join(producer, NULL);
	pthread_barrier_destroy(&start);
	spsc_destroy(&queue);

	printf("spsc: %llu messages in %.3fs\n", MESSAGES, elapsed);
	printf("spsc: %.1f Mops/s (checksum %llu)\n", (double)MESSAGES / elapsed / 1e6,
	       (unsigned long long)checksum);
	return 0;
}
