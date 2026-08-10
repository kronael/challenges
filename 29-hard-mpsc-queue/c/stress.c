// Each producer pushes a disjoint block of values, so the whole run pushes
// 1..PRODUCERS*MSGS, each exactly once. Asserting every value comes back exactly
// once — not merely that each of 1..MSGS returns PRODUCERS times — catches a lost
// item masked by a duplicate of the same message, which leaves both the total and
// a per-value-multiplicity count unchanged.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define PRODUCERS 8
#define MSGS 100000u

static MpscQueue queue;
static pthread_barrier_t start;

static void *producer_fn(void *arg) {
	uint64_t base = (uint64_t)(intptr_t)arg * MSGS;  // this producer's disjoint block
	pthread_barrier_wait(&start);
	for (uint64_t i = 1; i <= MSGS; i++) {
		mpsc_push(&queue, base + i);
	}
	return NULL;
}

int main(void) {
	mpsc_init(&queue);
	pthread_barrier_init(&start, NULL, PRODUCERS);

	pthread_t producers[PRODUCERS];
	for (int i = 0; i < PRODUCERS; i++) {
		if (pthread_create(&producers[i], NULL, producer_fn, (void *)(intptr_t)i) != 0) {
			perror("pthread_create");
			return 1;
		}
	}

	uint64_t total_vals = (uint64_t)PRODUCERS * MSGS;
	uint32_t *counts = (uint32_t *)calloc(total_vals + 1, sizeof *counts);
	if (counts == NULL) {
		perror("calloc");
		return 1;
	}

	unsigned long long remaining = total_vals;
	while (remaining > 0) {
		uint64_t value;
		if (mpsc_try_pop(&queue, &value) != POP_ITEM) {
			continue;
		}
		if (value == 0 || value > total_vals) {
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

	for (uint64_t value = 1; value <= total_vals; value++) {
		if (counts[value] != 1) {
			fprintf(stderr, "FAIL: value %llu popped %u times, expected exactly once\n",
				(unsigned long long)value, counts[value]);
			return 1;
		}
	}

	free(counts);
	pthread_barrier_destroy(&start);
	mpsc_destroy(&queue);
	printf("ok: %d producers x %u messages, no loss and no duplication\n", PRODUCERS, MSGS);
	return 0;
}
