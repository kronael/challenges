# 07 — Sense-Reversing Barrier

Reusable N-thread barrier from atomics only — no Mutex, Condvar, or OS sleep.
Hard because a naive "spin until count == N, then reset" barrier cannot be reused: a fast thread loops into round K+1 and sees the not-yet-reset count still at N, sailing through before its peers arrive.

## Teaches

- **Barrier reuse**: a shared count alone can't distinguish phase K from K+1, so a stale count leaks across rounds and releases threads early.
- **Sense reversal**: each thread holds a local sense bit; the last arriver resets the count and flips a shared sense; others spin on the *flipped bit*, not the count, so a stale count can never release them.
- **Fence ordering**: a `fence(Release)` over the count-reset and sense-flip (Acquire on waiters) guarantees peers see the reset before the flip — plain `Relaxed` stores do not.

## Run
```
cd rust && make
cd go   && make
```
Source: [Mellor-Crummey & Scott, *Algorithms for Scalable Synchronization* (ACM TOCS 1991)](https://www.cs.rochester.edu/u/scott/papers/1991_TOCS_synch.pdf)
