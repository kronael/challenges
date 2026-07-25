// Throughput: the owner pushes and pops while thieves drain the other end.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define TASKS 2000000u
#define THIEVES 3

static Deque deque;
static pthread_barrier_t start;
static _Atomic int stop = 0;
static _Atomic unsigned long long consumed = 0;

static void *thief_fn(void *arg) {
	(void)arg;
	unsigned long long local = 0;
	pthread_barrier_wait(&start);
	for (;;) {
		uint64_t value;
		StealStatus status = deque_steal(&deque, &value);
		if (status == STEAL_SUCCESS) {
			local++;
		} else if (status == STEAL_EMPTY &&
			   atomic_load_explicit(&stop, memory_order_acquire) != 0) {
			break;
		}
	}
	atomic_fetch_add_explicit(&consumed, local, memory_order_relaxed);
	return NULL;
}

static double now_seconds(void) {
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

int main(void) {
	deque_init(&deque);
	pthread_barrier_init(&start, NULL, THIEVES + 1);

	pthread_t thieves[THIEVES];
	for (int i = 0; i < THIEVES; i++) {
		pthread_create(&thieves[i], NULL, thief_fn, NULL);
	}

	pthread_barrier_wait(&start);
	double t0 = now_seconds();
	unsigned long long owner_took = 0;
	for (uint64_t task = 1; task <= TASKS; task++) {
		deque_push(&deque, task);
		if (task % 3 == 0) {
			uint64_t value;
			if (deque_pop(&deque, &value)) {
				owner_took++;
			}
		}
	}
	uint64_t value;
	while (deque_pop(&deque, &value)) {
		owner_took++;
	}
	atomic_store_explicit(&stop, 1, memory_order_release);
	double elapsed = now_seconds() - t0;

	for (int i = 0; i < THIEVES; i++) {
		pthread_join(thieves[i], NULL);
	}
	pthread_barrier_destroy(&start);
	deque_destroy(&deque);

	unsigned long long stolen = atomic_load_explicit(&consumed, memory_order_relaxed);
	printf("deque: %u tasks, %d thieves in %.3fs\n", TASKS, THIEVES, elapsed);
	printf("deque: %.1f Mtasks/s (owner %llu, stolen %llu)\n", (double)TASKS / elapsed / 1e6,
	       owner_took, stolen);
	return 0;
}
