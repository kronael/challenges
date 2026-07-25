// Every producer pushes 1..MSGS, so each value must come back out exactly
// PRODUCERS times. Checking the whole multiset — not just the total — catches a
// lost item paired with a duplicated one, which leaves the sum unchanged.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define PRODUCERS 8
#define MSGS 100000u

static MpscQueue queue;
static pthread_barrier_t start;

static void *producer_fn(void *arg) {
	(void)arg;
	pthread_barrier_wait(&start);
	for (uint64_t value = 1; value <= MSGS; value++) {
		mpsc_push(&queue, value);
	}
	return NULL;
}

int main(void) {
	mpsc_init(&queue);
	pthread_barrier_init(&start, NULL, PRODUCERS);

	pthread_t producers[PRODUCERS];
	for (int i = 0; i < PRODUCERS; i++) {
		if (pthread_create(&producers[i], NULL, producer_fn, NULL) != 0) {
			perror("pthread_create");
			return 1;
		}
	}

	uint32_t *counts = (uint32_t *)calloc(MSGS + 1, sizeof *counts);
	if (counts == NULL) {
		perror("calloc");
		return 1;
	}

	unsigned long long remaining = (unsigned long long)PRODUCERS * MSGS;
	while (remaining > 0) {
		uint64_t value;
		if (mpsc_try_pop(&queue, &value) != POP_ITEM) {
			continue;
		}
		if (value == 0 || value > MSGS) {
			fprintf(stderr, "FAIL: popped out-of-range value %llu\n",
				(unsigned long long)value);
			return 1;
		}
		counts[value]++;
		remaining--;
	}

	for (int i = 0; i < PRODUCERS; i++) {
		pthread_join(producers[i], NULL);
	}

	uint64_t leftover;
	switch (mpsc_try_pop(&queue, &leftover)) {
	case POP_EMPTY:
		break;
	case POP_ITEM:
		fprintf(stderr, "FAIL: extra item %llu after draining every message\n",
			(unsigned long long)leftover);
		return 1;
	case POP_RETRY:
		fprintf(stderr, "FAIL: POP_RETRY after every producer joined\n");
		return 1;
	}

	for (uint64_t value = 1; value <= MSGS; value++) {
		if (counts[value] != PRODUCERS) {
			fprintf(stderr, "FAIL: value %llu popped %u times, expected %d\n",
				(unsigned long long)value, counts[value], PRODUCERS);
			return 1;
		}
	}

	free(counts);
	pthread_barrier_destroy(&start);
	mpsc_destroy(&queue);
	printf("ok: %d producers x %u messages, no loss and no duplication\n", PRODUCERS, MSGS);
	return 0;
}
