// ROTTEN: plain slot-by-slot copies have no sequence counter, so a reader can
// combine two ticks. Stress pauses the writer halfway through a copy and reads
// the payload, making the torn snapshot deterministic.

#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    double v[8];
} Tick;

static volatile Tick data;
static _Atomic int pause_halfway;
static _Atomic int stage;

static void write_tick(const Tick *src) {
    // Naive: overwrite eight independent slots with no version marker. Correct
    // alone, but a concurrent read can observe any prefix of the new tick.
    for (int i = 0; i < 8; i++) {
        data.v[i] = src->v[i];
        if (i == 3 && atomic_load_explicit(&pause_halfway, memory_order_relaxed)) {
            atomic_store_explicit(&stage, 1, memory_order_release);
            while (atomic_load_explicit(&stage, memory_order_acquire) != 2) {
            }
        }
    }
}

static int read_tick(Tick *dst) {
    for (int i = 0; i < 8; i++) dst->v[i] = data.v[i];
    return 1;
}

static int consistent(const Tick *tick) {
    for (int i = 1; i < 8; i++)
        if (tick->v[i] != tick->v[0]) return 0;
    return 1;
}

static int weak_sanity(void) {
    Tick in;
    Tick out;
    for (int i = 0; i < 8; i++) in.v[i] = 7.0;
    write_tick(&in);
    read_tick(&out);
    if (!consistent(&out) || out.v[0] != 7.0) return 1;
    puts("PASS");
    return 0;
}

static void *writer(void *raw) {
    write_tick(raw);
    return NULL;
}

static int adversarial_stress(void) {
    Tick next;
    Tick observed;
    for (int i = 0; i < 8; i++) next.v[i] = 1.0;
    atomic_store_explicit(&pause_halfway, 1, memory_order_relaxed);
    atomic_store_explicit(&stage, 0, memory_order_relaxed);

    pthread_t thread;
    pthread_create(&thread, NULL, writer, &next);
    while (atomic_load_explicit(&stage, memory_order_acquire) != 1) {
    }
    read_tick(&observed);
    atomic_store_explicit(&stage, 2, memory_order_release);
    pthread_join(thread, NULL);

    if (!consistent(&observed)) {
        fputs("FAIL: reader accepted a torn snapshot\n", stderr);
        return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "stress") == 0) return adversarial_stress();
    return weak_sanity();
}
