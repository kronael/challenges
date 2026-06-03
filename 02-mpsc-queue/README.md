# 02 — Vyukov MPSC Queue

Intrusive lock-free queue: many producers `push`, one consumer `try_pop`, atomics only.
Hard because `push` swaps the head then links the predecessor as two separate steps, leaving a window where the queue holds an already-enqueued node that no consumer can reach.

## Teaches

- **Vyukov's broken-link window**: `prev = head.swap(node)` then `prev.next = node` is non-atomic; between them the new node *is* the head but is unreachable from the tail.
- **3-valued pop**: `tail.next == null` with `tail != head` means a producer is mid-link — return `Retry`, never `Empty`, or already-enqueued messages are lost.
- **Ordering**: head swap is `AcqRel`, the `next` publish is `Release`, the consumer reads with `Acquire`.

## Run
```
cd rust && make
cd go   && make
```
Source: [1024cores.net — Intrusive MPSC node-based queue](https://www.1024cores.net/home/lock-free-algorithms/queues/intrusive-mpsc-node-based-queue)
