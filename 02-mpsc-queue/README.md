# 02 — Vyukov MPSC Queue

**Task**: Implement a lock-free multi-producer single-consumer queue where `push` is wait-free (no CAS loop) and `try_pop` distinguishes "the queue is empty" from "a producer is mid-enqueue".

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

Any number of threads may call `push` simultaneously; exactly one thread calls
`try_pop`. A producer enqueues a node in more than one step, and there is a
window in the middle of an enqueue where a freshly added node has been attached
at one end but is not yet reachable from the other. A consumer that looks during
that window sees an apparently empty list even though a message is already in
flight.

This is the trap: if `try_pop` reports "empty" the instant it sees no reachable
node, an already-enqueued message is dropped forever — the stress test pushes
millions of values and a single lost one fails it. So `try_pop` must be
*three-valued*: it returns the item, or "empty" (no producer is enqueuing and
nothing is pending), or "retry" (a producer is mid-enqueue; the caller should
spin and try again). Telling the genuine-empty case apart from the
mid-enqueue case is the whole problem — and it is what separates this from a
trivial mutex-guarded queue.

`push` must be wait-free: no CAS retry loop, no blocking, bounded steps
regardless of contention. The stress test runs many producers against one
consumer and asserts every pushed message is popped exactly once — none lost,
none duplicated.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.

Source: [1024cores.net — Intrusive MPSC node-based queue](https://www.1024cores.net/home/lock-free-algorithms/queues/intrusive-mpsc-node-based-queue)
