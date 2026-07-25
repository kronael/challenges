// Two barriers bracket a critical section each round. Between them every thread
// stamps the round number into its own slot; after the closing barrier it reads
// all N slots, which must all hold the current round.
//
// Released early -> a peer has not stamped yet and the reader sees a stale slot.
// Never released -> every peer stalls and the harness kills the run on timeout.

#include "solution.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define N 16
#define ROUNDS 100000

static SpinBarrier barrier;
static _Atomic long slots[N];
static _Atomic long early = 0;

typedef struct {
	int id;
} Args;

static void *worker(void *p) {
	const Args *args = (const Args *)p;
	int local_sense = 0;
	for (long round = 0; round < ROUNDS; round++) {
		barrier_wait(&barrier, &local_sense);
		atomic_store_explicit(&slots[args->id], round, memory_order_relaxed);
		barrier_wait(&barrier, &local_sense);
		for (int i = 0; i < N; i++) {
			if (atomic_load_explicit(&slots[i], memory_order_relaxed) != round) {
				atomic_fetch_add_explicit(&early, 1, memory_order_relaxed);
			}
		}
	}
	return NULL;
}

int main(void) {
	barrier_init(&barrier, N);
	for (int i = 0; i < N; i++) {
		atomic_store_explicit(&slots[i], -1, memory_order_relaxed);
	}

	pthread_t threads[N];
	Args args[N];
	for (int i = 0; i < N; i++) {
		args[i].id = i;
		if (pthread_create(&threads[i], NULL, worker, &args[i]) != 0) {
			perror("pthread_create");
			return 1;
		}
	}
	for (int i = 0; i < N; i++) {
		pthread_join(threads[i], NULL);
	}

	long violations = atomic_load_explicit(&early, memory_order_relaxed);
	if (violations != 0) {
		fprintf(stderr, "FAIL: %ld stale slots — a thread passed before all %d arrived\n",
			violations, N);
		return 1;
	}
	printf("ok: %d threads x %d rounds, nobody passed early\n", N, ROUNDS);
	return 0;
}
