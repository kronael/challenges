# 05 — SPSC Ring Buffer

**Task**: Implement a single-producer single-consumer ring buffer that sustains
1B+ messages/second, and find why the obvious correct version is still too slow.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

Implement a bounded, lock-free queue between exactly two threads: one producer
that only ever pushes, one consumer that only ever pops. Capacity `N` is a power
of two. `push` returns false when the queue is full; `pop` returns nothing when
it is empty. Every value the producer enqueues must come back to the consumer
exactly once, in order — no loss, no duplicates, no reordering.

Correctness is the easy part: with exactly one writer on the producer side and
exactly one writer on the consumer side, a straightforward implementation can
deliver every message in order without a lock. The trap is performance. The
producer and consumer both update their own small piece of shared state on every
operation; a version that is logically correct can still force the two cores to
coordinate far more often than the data flow requires.

The target is 1B+ messages/second. The stress test pushes many messages and
asserts in-order delivery; the bench measures throughput. The obvious correct
version is several times too slow, and the job is to find out why and fix it
without adding a lock.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.

Source: [Drepper, *What Every Programmer Should Know About Memory*](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)
