# 07 — Sense-Reversing Barrier

**Task**: Implement a reusable N-thread spin barrier from atomics only — no Mutex, Condvar, or OS sleep — that works correctly across many phases.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

A barrier blocks each thread until all N have arrived, then releases them
together. The naive version — "increment a count, spin until count == N, then
reset" — cannot be reused: a fast thread that loops into phase K+1 sees the
not-yet-reset count still at N and sails straight through before its peers from
phase K have even left.

Sense reversal fixes this with a local sense bit per thread plus a shared sense
bit. The last arriver resets the count and *flips* the shared sense; everyone
else spins on the flipped bit, not the count — so a stale count can never release
them. The stress test runs N threads through many phases and asserts no thread
ever runs ahead.

## Teaches

- **Barrier reuse**: a shared count alone can't distinguish phase K from K+1, so a stale count leaks across rounds and releases threads early.
- **Sense reversal**: each thread holds a local sense bit; the last arriver resets the count and flips a shared sense; others spin on the *flipped bit*, so a stale count can never release them.
- **Fence ordering**: a `fence(Release)` over the count-reset and sense-flip (Acquire on waiters) guarantees peers see the reset before the flip — plain `Relaxed` stores do not.

## Run

```
cd rust && make test
cd go   && make test
```

Source: [Mellor-Crummey & Scott, *Algorithms for Scalable Synchronization* (ACM TOCS 1991)](https://www.cs.rochester.edu/u/scott/papers/1991_TOCS_synch.pdf)
