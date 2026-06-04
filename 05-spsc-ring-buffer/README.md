# 05 — SPSC Ring Buffer

**Task**: Implement a single-producer single-consumer ring buffer that sustains 1B+ messages/second — and find why the obvious correct version is 3–5x too slow.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

Implement a bounded, lock-free queue between exactly two threads: one producer
that only ever pushes, one consumer that only ever pops. Capacity `N` is a power
of two. `push` returns false when the queue is full; `pop` returns nothing when
it is empty. Every value the producer enqueues must come back to the consumer
exactly once, in order — no loss, no duplicates, no reordering.

Correctness is the easy part: with one writer per index and no locks, a
straightforward implementation can be made to deliver every message in order.
The trap is performance. The producer writes its index on every push and the
consumer writes its index on every pop. If those two indices happen to live
close together in memory, the two cores end up fighting over the same chunk of
cache on every single operation — even though neither thread reads the other's
index most of the time. The threads serialise through the cache-coherence
protocol and throughput collapses to a fraction of what the hardware can do.

The target is 1B+ messages/second. The stress test pushes billions of messages
and asserts in-order delivery; the bench measures throughput. The obvious
correct version is 3–5x too slow, and the job is to find out why and fix it
without adding a lock.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.

Source: [Drepper, *What Every Programmer Should Know About Memory* §6.4 (false sharing)](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)
