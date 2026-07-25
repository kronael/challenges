// Each pop must return the next value the producer sent. Equality at every
// position rules out skips, duplicates and reordering in one check; the loop
// count rules out loss.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define MESSAGES 10000000ull
#define CAP 4096

static SpscQueue queue;
static pthread_barrier_t start;
static _Atomic int failed = 0;

static void *producer_fn(void *arg) {
	(void)arg;
	pthread_barrier_wait(&start);
	for (uint64_t value = 0; value < MESSAGES; value++) {
		while (!spsc_push(&queue, value)) {
		}
	}
	return NULL;
}

static void *consumer_fn(void *arg) {
	(void)arg;
	pthread_barrier_wait(&start);
	for (uint64_t expected = 0; expected < MESSAGES; expected++) {
		uint64_t value;
		while (!spsc_pop(&queue, &value)) {
		}
		if (value != expected) {
			fprintf(stderr, "FAIL: got %llu at position %llu\n",
				(unsigned long long)value, (unsigned long long)expected);
			atomic_store_explicit(&failed, 1, memory_order_relaxed);
			return NULL;
		}
	}
	return NULL;
}

static int backpressure(void) {
	SpscQueue small;
	spsc_init(&small, 8);

	uint64_t pushed = 0;
	while (spsc_push(&small, pushed)) {
		pushed++;
		if (pushed > 8) {
			fprintf(stderr, "FAIL: pushed past capacity — full not detected\n");
			return 1;
		}
	}
	// Either boundary is fine: a full-detection scheme may keep one slot spare.
	if (pushed != 8 && pushed != 7) {
		fprintf(stderr, "FAIL: filled %llu of 8 slots\n", (unsigned long long)pushed);
		return 1;
	}
	for (uint64_t expected = 0; expected < pushed; expected++) {
		uint64_t value;
		if (!spsc_pop(&small, &value) || value != expected) {
			fprintf(stderr, "FAIL: out-of-order drain after full\n");
			return 1;
		}
	}
	uint64_t leftover;
	if (spsc_pop(&small, &leftover)) {
		fprintf(stderr, "FAIL: queue not empty after a full drain\n");
		return 1;
	}
	spsc_destroy(&small);
	return 0;
}

int main(void) {
	spsc_init(&queue, CAP);
	pthread_barrier_init(&start, NULL, 2);

	pthread_t producer, consumer;
	if (pthread_create(&producer, NULL, producer_fn, NULL) != 0 ||
	    pthread_create(&consumer, NULL, consumer_fn, NULL) != 0) {
		perror("pthread_create");
		return 1;
	}
	pthread_join(producer, NULL);
	pthread_join(consumer, NULL);
	pthread_barrier_destroy(&start);

	if (atomic_load_explicit(&failed, memory_order_relaxed) != 0) {
		return 1;
	}

	uint64_t leftover;
	if (spsc_pop(&queue, &leftover)) {
		fprintf(stderr, "FAIL: queue not empty after every message was received\n");
		return 1;
	}
	spsc_destroy(&queue);

	if (backpressure() != 0) {
		return 1;
	}
	printf("ok: %llu messages delivered in order, backpressure honoured\n", MESSAGES);
	return 0;
}
