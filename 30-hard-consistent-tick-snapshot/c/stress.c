// The writer stamps one counter into all eight u64 slots of the payload, so any
// snapshot whose slots disagree was assembled from two different epochs.
// max_seen proves the readers observed real, advancing values, so a writer that
// never publishes cannot pass by keeping the payload trivially consistent.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define READERS 15
#define READER_ITERS 2000000u
#define SLOTS (TICK_BYTES / (int)sizeof(uint64_t))

static Seqlock lock;
static pthread_barrier_t start;
static _Atomic int stop = 0;
static _Atomic uint64_t torn = 0;
static _Atomic uint64_t max_seen = 0;
static _Atomic uint64_t written = 0;

static void pack(unsigned char *buf, uint64_t counter) {
	for (int slot = 0; slot < SLOTS; slot++) {
		memcpy(buf + slot * sizeof counter, &counter, sizeof counter);
	}
}

// Returns true and stores the shared slot value when all eight slots agree;
// returns false when they disagree (a torn snapshot). Value 0 is a legitimate
// snapshot — the initial pre-publication state — and must not read as torn.
static bool consistent_value(const unsigned char *buf, uint64_t *out) {
	uint64_t first;
	memcpy(&first, buf, sizeof first);
	for (int slot = 1; slot < SLOTS; slot++) {
		uint64_t value;
		memcpy(&value, buf + slot * sizeof value, sizeof value);
		if (value != first) {
			return false;
		}
	}
	*out = first;
	return true;
}

static void *writer_fn(void *arg) {
	(void)arg;
	unsigned char buf[TICK_BYTES];
	pthread_barrier_wait(&start);
	uint64_t counter = 1;
	while (atomic_load_explicit(&stop, memory_order_relaxed) == 0) {
		pack(buf, counter);
		seqlock_write(&lock, buf);
		counter++;
	}
	atomic_store_explicit(&written, counter, memory_order_relaxed);
	return NULL;
}

static void *reader_fn(void *arg) {
	(void)arg;
	unsigned char buf[TICK_BYTES];
	uint64_t local_max = 0;
	pthread_barrier_wait(&start);
	for (unsigned i = 0; i < READER_ITERS; i++) {
		while (!seqlock_read(&lock, buf)) {
		}
		uint64_t value;
		if (!consistent_value(buf, &value)) {
			atomic_fetch_add_explicit(&torn, 1, memory_order_relaxed);
		} else if (value > local_max) {
			local_max = value;
		}
	}
	uint64_t seen = atomic_load_explicit(&max_seen, memory_order_relaxed);
	while (local_max > seen &&
	       !atomic_compare_exchange_weak_explicit(&max_seen, &seen, local_max,
						      memory_order_relaxed, memory_order_relaxed)) {
	}
	return NULL;
}

int main(void) {
	seqlock_init(&lock);
	pthread_barrier_init(&start, NULL, READERS + 1);

	pthread_t writer;
	pthread_t readers[READERS];
	if (pthread_create(&writer, NULL, writer_fn, NULL) != 0) {
		perror("pthread_create");
		return 1;
	}
	for (int i = 0; i < READERS; i++) {
		if (pthread_create(&readers[i], NULL, reader_fn, NULL) != 0) {
			perror("pthread_create");
			return 1;
		}
	}
	for (int i = 0; i < READERS; i++) {
		pthread_join(readers[i], NULL);
	}
	atomic_store_explicit(&stop, 1, memory_order_relaxed);
	pthread_join(writer, NULL);
	pthread_barrier_destroy(&start);

	uint64_t tears = atomic_load_explicit(&torn, memory_order_relaxed);
	if (tears != 0) {
		fprintf(stderr, "FAIL: %llu torn reads — payload tore between epochs\n",
			(unsigned long long)tears);
		return 1;
	}
	if (atomic_load_explicit(&written, memory_order_relaxed) <= 1) {
		fprintf(stderr, "FAIL: the writer never advanced the sequence\n");
		return 1;
	}
	if (atomic_load_explicit(&max_seen, memory_order_relaxed) == 0) {
		fprintf(stderr, "FAIL: readers never observed a written value\n");
		return 1;
	}
	printf("ok: %d readers x %u reads, no torn snapshot\n", READERS, READER_ITERS);
	return 0;
}
