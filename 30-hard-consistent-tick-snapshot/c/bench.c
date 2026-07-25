// Throughput: one writer publishing while readers snapshot as fast as they can.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define READERS 4
#define READER_ITERS 5000000u

static Seqlock lock;
static pthread_barrier_t start;
static _Atomic int stop = 0;

static void *writer_fn(void *arg) {
	(void)arg;
	unsigned char buf[TICK_BYTES];
	memset(buf, 0, sizeof buf);
	pthread_barrier_wait(&start);
	uint64_t counter = 1;
	while (atomic_load_explicit(&stop, memory_order_relaxed) == 0) {
		memcpy(buf, &counter, sizeof counter);
		seqlock_write(&lock, buf);
		counter++;
	}
	return NULL;
}

static void *reader_fn(void *arg) {
	(void)arg;
	unsigned char buf[TICK_BYTES];
	pthread_barrier_wait(&start);
	for (unsigned i = 0; i < READER_ITERS; i++) {
		while (!seqlock_read(&lock, buf)) {
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
	seqlock_init(&lock);
	pthread_barrier_init(&start, NULL, READERS + 1);

	pthread_t writer;
	pthread_t readers[READERS];
	pthread_create(&writer, NULL, writer_fn, NULL);
	for (int i = 0; i < READERS; i++) {
		pthread_create(&readers[i], NULL, reader_fn, NULL);
	}

	double t0 = now_seconds();
	for (int i = 0; i < READERS; i++) {
		pthread_join(readers[i], NULL);
	}
	double elapsed = now_seconds() - t0;
	atomic_store_explicit(&stop, 1, memory_order_relaxed);
	pthread_join(writer, NULL);
	pthread_barrier_destroy(&start);

	double reads = (double)READERS * READER_ITERS;
	printf("seqlock: %d readers, %.0f snapshots in %.3fs\n", READERS, reads, elapsed);
	printf("seqlock: %.1f Mreads/s\n", reads / elapsed / 1e6);
	return 0;
}
