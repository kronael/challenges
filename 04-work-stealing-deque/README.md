# 04 — Chase-Lev Work-Stealing Deque

**Task**: Implement a deque where the owner pushes and pops at the bottom while any number of thieves steal from the top, all with atomics only.

**Difficulty**: expert
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

The hard part is the last element. When `bottom - top == 1`, exactly one slot
remains, and the owner's `pop` races a thief's `steal` for it. Two consumers may
both look at that slot and each conclude it is theirs — and then the same task is
returned twice, or, if both back off, lost. The invariant you must hold under
arbitrary interleaving and on a weak memory model: every task that goes in comes
out exactly once, across the owner and all thieves combined, with no torn or
duplicated value.

The backing buffer is fixed power-of-two sized; you do not need to resize it.
The stress test runs one owner against many thieves, interleaving pushes with
the owner's own pops so the deque hovers at one element, then asserts that the
multiset of everything consumed equals the multiset pushed — a repeat means two
threads claimed the same element, a gap means one was dropped.

## Run

```
cd rust && make test
```

Stuck? See `HINTS.md`.

Source: [Chase & Lev, *Dynamic Circular Work-Stealing Deque* (SPAA 2005)](https://www.di.ens.fr/~zappa/readings/ppopp13.pdf)
