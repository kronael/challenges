# 05 — Two-Thread Buffer

**Task**: Implement a bounded single-producer single-consumer buffer that
sustains 1B+ messages/second.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

Implement a bounded, lock-free buffer between exactly two threads: one producer
that only ever pushes, one consumer that only ever pops. Capacity `N` is a power
of two. `push` returns false when the queue is full; `pop` returns nothing when
it is empty. Every value the producer enqueues must come back to the consumer
exactly once, in order — no loss, no duplicates, no reordering.

The target is 1B+ messages/second. The stress test pushes many messages and
asserts in-order delivery; the bench measures throughput.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.
