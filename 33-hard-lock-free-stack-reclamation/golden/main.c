// Treiber stack with hazard-pointer reclamation. No GC, no leaks, no UAF.
// A popper guesses head, publishes it to its hazard slot (seq_cst), then
// re-validates head is unchanged before dereferencing — the reclaimer only
// frees a node no hazard slot points at. seq_cst on publish-then-verify closes
// the TOCTOU window that Release/Acquire would leave open. Freed memory is
// poisoned (high bits set, outside the task-value range) so any use-after-free
// trips the claim check. Stress: 8 threads each push 10k and pop 10k concurrently.
//
// Lifetime invariant the popper must hold (the subtle part): hazard[tid] always
// names the node this thread is *currently* dereferencing, or NULL. Every exit
// from pop that is not a successful claim clears the slot first — a stale hazard
// would either pin a node forever (leak) or, worse, let the thread later trust a
// slot it no longer guards. Reclamation runs only after a barrier, when no thread
// holds a hazard, so a retired node is freed exactly once with no live reader.
#define _POSIX_C_SOURCE 200809L  // pthread_barrier_* under -std=c11
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define NTHREADS 8
#define PER_THREAD 10000u
#define NTASKS (NTHREADS * PER_THREAD)
#define RETIRE_THRESH 64  // scan + reclaim once a thread's retire list hits this
#define RETIRE_CAP 4096   // > worst-case survivors between scans
#define POISON 0xDEAD000000000000ull  // high bits: cannot collide with a task value

typedef struct Node {
    _Atomic(struct Node *) next;
    uint64_t val;
} Node;

static _Atomic(Node *) stack_head = NULL;
static _Atomic(Node *) hazard[NTHREADS];  // one published pointer per thread

static _Atomic uint64_t allocs = 0;  // leak / double-free accounting
static _Atomic uint64_t frees = 0;

static Node *alloc_node(uint64_t v) {
    Node *n = malloc(sizeof(Node));
    if (!n) {
        fprintf(stderr, "FAIL: malloc\n");
        exit(1);
    }
    atomic_store_explicit(&n->next, NULL, memory_order_relaxed);
    n->val = v;
    atomic_fetch_add_explicit(&allocs, 1, memory_order_relaxed);
    return n;
}

static void free_node(Node *n) {
    n->val = POISON;  // a later use-after-free read sees garbage, not a real task
    atomic_store_explicit(&n->next, (Node *)(uintptr_t)POISON, memory_order_relaxed);
    atomic_fetch_add_explicit(&frees, 1, memory_order_relaxed);
    free(n);
}

static void push(uint64_t v) {
    Node *n = alloc_node(v);
    Node *h = atomic_load_explicit(&stack_head, memory_order_relaxed);
    do {
        atomic_store_explicit(&n->next, h, memory_order_relaxed);
    } while (!atomic_compare_exchange_weak_explicit(&stack_head, &h, n,
                                                    memory_order_release, memory_order_relaxed));
}

// Per-thread retire list, scanned against all hazard slots.
typedef struct {
    Node *buf[RETIRE_CAP];
    int n;
} Retire;

// Free each retired node no hazard slot currently guards; keep the rest.
static void scan(Retire *r) {
    Node *haz[NTHREADS];
    int nh = 0;
    for (int i = 0; i < NTHREADS; i++) {
        Node *p = atomic_load_explicit(&hazard[i], memory_order_seq_cst);
        if (p) haz[nh++] = p;
    }
    int kept = 0;
    for (int i = 0; i < r->n; i++) {
        Node *node = r->buf[i];
        int hazardous = 0;
        for (int j = 0; j < nh; j++) {
            if (haz[j] == node) {
                hazardous = 1;
                break;
            }
        }
        if (hazardous)
            r->buf[kept++] = node;  // still guarded — try again on the next scan
        else
            free_node(node);
    }
    r->n = kept;
}

static void retire(Retire *r, Node *n) {
    r->buf[r->n++] = n;
    if (r->n >= RETIRE_THRESH) scan(r);
}

// Returns 1 and writes *out on success, 0 if the stack was empty.
static int pop(int tid, uint64_t *out, Retire *r) {
    for (;;) {
        Node *h = atomic_load_explicit(&stack_head, memory_order_acquire);  // guess
        if (!h) {
            atomic_store_explicit(&hazard[tid], NULL, memory_order_seq_cst);  // invariant
            return 0;
        }
        atomic_store_explicit(&hazard[tid], h, memory_order_seq_cst);  // publish
        atomic_thread_fence(memory_order_seq_cst);
        // verify: if head moved, our guess may already be retired — retry (slot
        // is re-published with the fresh guess next iteration).
        if (atomic_load_explicit(&stack_head, memory_order_seq_cst) != h) continue;
        // h is hazard-protected now: no scanner will free it under us.
        Node *next = atomic_load_explicit(&h->next, memory_order_acquire);
        if (atomic_compare_exchange_strong_explicit(&stack_head, &h, next,
                                                    memory_order_seq_cst, memory_order_relaxed)) {
            *out = h->val;  // read while still hazard-protected
            atomic_store_explicit(&hazard[tid], NULL, memory_order_seq_cst);  // unpublish
            retire(r, h);
            return 1;
        }
        // lost the CAS; loop and re-guess (slot overwritten on next publish)
    }
}

static _Atomic uint64_t claimed[NTASKS];  // claimed[v]++ on each pop
static pthread_barrier_t phase;           // separates concurrent run from reclamation

// Retired nodes a thread couldn't reclaim by exit; main frees them post-join,
// once every thread is gone and no hazard remains.
static Node *leftover[NTHREADS][RETIRE_CAP];
static int leftover_n[NTHREADS];

typedef struct {
    int tid;
} Arg;

static void take(uint64_t v) {
    if (v == POISON || v >= NTASKS) {
        fprintf(stderr, "FAIL: popped poisoned/oob value %llu\n", (unsigned long long)v);
        exit(1);
    }
    atomic_fetch_add_explicit(&claimed[v], 1, memory_order_relaxed);
}

static void *worker(void *p) {
    int tid = ((Arg *)p)->tid;
    Retire r = {.n = 0};
    uint64_t base = (uint64_t)tid * PER_THREAD;

    pthread_barrier_wait(&phase);

    // Each thread pushes PER_THREAD and pops PER_THREAD, interleaved, so total
    // pushes == total pops and the stack is empty once everyone is done.
    for (uint64_t i = 0; i < PER_THREAD; i++) push(base + i);
    for (uint64_t i = 0; i < PER_THREAD; i++) {
        uint64_t v;
        // The stack holds NTASKS items total; with everyone popping there is
        // always one for us — spin only on transient CAS losses.
        while (!pop(tid, &v, &r)) { /* spin: another thread is mid-update */ }
        take(v);
    }

    // Hand our still-unreclaimed retired nodes to main (freed after all joins).
    for (int i = 0; i < r.n; i++) leftover[tid][i] = r.buf[i];
    leftover_n[tid] = r.n;
    return NULL;
}

int main(void) {
    for (int i = 0; i < NTHREADS; i++)
        atomic_store_explicit(&hazard[i], NULL, memory_order_relaxed);

    pthread_t th[NTHREADS];
    Arg args[NTHREADS];
    pthread_barrier_init(&phase, NULL, NTHREADS);

    for (int i = 0; i < NTHREADS; i++) {
        args[i].tid = i;
        pthread_create(&th[i], NULL, worker, &args[i]);
    }
    for (int i = 0; i < NTHREADS; i++) pthread_join(th[i], NULL);

    // Quiescent: no thread holds a hazard, so every leftover is reclaimable.
    for (int i = 0; i < NTHREADS; i++)
        for (int k = 0; k < leftover_n[i]; k++) free_node(leftover[i][k]);

    if (atomic_load_explicit(&stack_head, memory_order_seq_cst) != NULL) {
        fprintf(stderr, "FAIL: stack not empty\n");
        return 1;
    }
    for (uint64_t i = 0; i < NTASKS; i++) {
        uint64_t c = atomic_load_explicit(&claimed[i], memory_order_relaxed);
        if (c != 1) {
            fprintf(stderr, "FAIL: value %llu popped %llu times (expected 1)\n",
                    (unsigned long long)i, (unsigned long long)c);
            return 1;
        }
    }
    uint64_t a = atomic_load_explicit(&allocs, memory_order_relaxed);
    uint64_t f = atomic_load_explicit(&frees, memory_order_relaxed);
    if (a != f) {
        fprintf(stderr, "FAIL: leak: %llu allocs vs %llu frees\n", (unsigned long long)a,
                (unsigned long long)f);
        return 1;
    }
    if (a != (uint64_t)NTASKS) {
        fprintf(stderr, "FAIL: expected %u allocs, got %llu\n", NTASKS, (unsigned long long)a);
        return 1;
    }

    pthread_barrier_destroy(&phase);
    printf("PASS\n");
    return 0;
}
