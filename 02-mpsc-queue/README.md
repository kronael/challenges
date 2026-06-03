# 02 — Vyukov MPSC Queue

**Task**: Implement a lock-free multi-producer single-consumer queue where `push` is wait-free (no CAS loop) and `try_pop` distinguishes "empty" from "a producer is mid-enqueue".

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

Any thread may call `push` simultaneously; exactly one thread calls `try_pop`.
The defining feature is that `push` links a node in *two* non-atomic steps —
`prev = head.swap(node)`, then `prev.next = node`. Between them the node is the
head yet unreachable from the tail. A consumer that hits this window must not
report `Empty`, or an already-enqueued message is lost forever.

So `try_pop` is three-valued: `Got(item)`, `Empty`, or `Retry` (a producer is
between its two steps). The Retry state is exactly what separates this from a
trivial mutex queue. The stress test runs many producers against one consumer and
asserts every pushed message is popped exactly once.

## Teaches

- **Vyukov's broken-link window**: `head.swap` then `prev.next = node` is non-atomic; in between, the node *is* the head but unreachable from the tail.
- **3-valued pop**: `tail.next == null` with `tail != head` means a producer is mid-link — return `Retry`, never `Empty`.
- **Ordering**: head swap is `AcqRel`, the `next` publish is `Release`, the consumer reads with `Acquire`.

## Run

```
cd rust && make test
cd go   && make test
```

Source: [1024cores.net — Intrusive MPSC node-based queue](https://www.1024cores.net/home/lock-free-algorithms/queues/intrusive-mpsc-node-based-queue)
