# 32 — Hard — Two-Thread Buffer

**Task**: Implement a bounded single-producer single-consumer buffer with a
non-blocking `push` and `pop` interface.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

Implement a bounded, lock-free buffer between exactly two threads: one producer
that only ever pushes, one consumer that only ever pops. Capacity `N` is a power
of two. `push` returns false when the queue is full; `pop` returns nothing when
it is empty. Every value the producer enqueues must come back to the consumer
exactly once, in order — no loss, no duplicates, no reordering.

The stress test pushes many messages and asserts in-order delivery. The bench
reports throughput for comparison between implementations.

## Run

```
make -C rust test
make -C go test
```

Stuck? See `HINTS.md`.
