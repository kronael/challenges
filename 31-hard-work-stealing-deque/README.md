# 31 — Hard — Concurrent Owner/Thief Deque

**Task**: Implement a deque where the owner pushes and pops at the bottom while any number of thieves steal from the top, all with atomics only.

**Difficulty**: hard
**Time estimate**: ~120 min

## Problem

This is the data structure behind every work-stealing scheduler: a worker runs
its own queue as a stack (bottom), and idle workers steal the oldest tasks (top).
Both ends operate concurrently and lock-free — no mutex on the hot path.

The interface is three operations:

- `push(task)` — owner only, adds at the bottom.
- `pop() -> Option<task>` — owner only, removes from the bottom (LIFO for the owner).
- `steal() -> Empty | Success(task) | Retry` — any thief, removes from the top
  (FIFO for thieves). `Retry` signals a transient race the caller should retry;
  `Empty` means there was nothing to take.

The backing buffer is fixed power-of-two sized; you do not need to resize it.
The stress test runs one owner against many thieves, interleaving pushes with
the owner's own pops, then asserts that the multiset of everything consumed
equals the multiset pushed.

## Run

```
cd rust && make test
```

Stuck? See `HINTS.md`.
