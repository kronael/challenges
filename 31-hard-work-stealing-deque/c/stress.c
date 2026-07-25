// The owner interleaves its own pops with pushes so the bottom hovers near the
// top, which is where a single element can be claimed by both the owner and a
// thief. Every task must be consumed exactly once across all consumers: a repeat
// means two threads claimed the same slot, a gap means one was dropped.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define TASKS 500000u
#define THIEVES 7

static Deque deque;
static pthread_barrier_t start;
static _Atomic int stop = 0;
static _Atomic unsigned *claimed;
static _Atomic int corrupt = 0;

static void claim(uint64_t value) {
	if (value < 1 || value > TASKS) {
		atomic_store_explicit(&corrupt, 1, memory_order_relaxed);
		return;
	}
	atomic_fetch_add_explicit(&claimed[value], 1, memory_order_relaxed);
}

static void *thief_fn(void *arg) {
	(void)arg;
	pthread_barrier_wait(&start);
	for (;;) {
		uint64_t value;
		switch (deque_steal(&deque, &value)) {
		case STEAL_SUCCESS:
			claim(value);
			break;
		case STEAL_RETRY:
			break;
		case STEAL_EMPTY:
			if (atomic_load_explicit(&stop, memory_order_acquire) != 0) {
				return NULL;
			}
			break;
		}
	}
}

int main(void) {
	deque_init(&deque);
	claimed = (_Atomic unsigned *)calloc(TASKS + 1, sizeof *claimed);
	if (claimed == NULL) {
		perror("calloc");
		return 1;
	}
	pthread_barrier_init(&start, NULL, THIEVES + 1);

	pthread_t thieves[THIEVES];
	for (int i = 0; i < THIEVES; i++) {
		if (pthread_create(&thieves[i], NULL, thief_fn, NULL) != 0) {
			perror("pthread_create");
			return 1;
		}
	}

	pthread_barrier_wait(&start);
	for (uint64_t task = 1; task <= TASKS; task++) {
		deque_push(&deque, task);
		if (task % 3 == 0) {
			uint64_t value;
			if (deque_pop(&deque, &value)) {
				claim(value);
			}
		}
	}
	uint64_t value;
	while (deque_pop(&deque, &value)) {
		claim(value);
	}

	atomic_store_explicit(&stop, 1, memory_order_release);
	for (int i = 0; i < THIEVES; i++) {
		pthread_join(thieves[i], NULL);
	}
	pthread_barrier_destroy(&start);

	if (atomic_load_explicit(&corrupt, memory_order_relaxed) != 0) {
		fprintf(stderr, "FAIL: a consumer returned a value outside 1..%u\n", TASKS);
		return 1;
	}
	for (uint64_t task = 1; task <= TASKS; task++) {
		unsigned times = atomic_load_explicit(&claimed[task], memory_order_relaxed);
		if (times != 1) {
			fprintf(stderr, "FAIL: task %llu consumed %u times, expected 1\n",
				(unsigned long long)task, times);
			return 1;
		}
	}

	free((void *)claimed);
	deque_destroy(&deque);
	printf("ok: %u tasks, owner + %d thieves, each task consumed exactly once\n", TASKS,
	       THIEVES);
	return 0;
}
