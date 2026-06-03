# 04 — Chase-Lev Work-Stealing Deque

**Task**: Implement a deque where the owner pushes and pops at the bottom while any number of thieves steal from the top, all with atomics only.

**Difficulty**: expert
**Time estimate**: ~120 min

## Problem

This is the data structure behind every work-stealing scheduler: a worker runs
its own queue as a stack (bottom), and idle workers steal the oldest tasks (top).
Both ends operate concurrently and lock-free.

The hard part is the last element. When `bottom - top == 1`, exactly one slot
remains, and the owner's `pop` races a thief's `steal` for it — exactly one may
win, and neither may return it twice. The owner speculatively decrements
`bottom`, reads the slot, then CASes `top`; the owner's `bottom` store and the
thief's `top` load form a Dekker pattern that only `SeqCst` on the decisive CAS
resolves correctly. The stress test runs one owner against many thieves and
asserts every task is taken exactly once.

## Teaches

- **Last-element race**: owner decrements `bottom`, reads the slot, then CASes `top`; on CAS failure a thief took it, so it returns Empty and restores `bottom`.
- **The Dekker moment**: the `bottom` store and the `top` load form a Dekker pattern — only `SeqCst` on the decisive `top` CAS stops both sides claiming the same element.
- **ABA**: `top` must carry a tag so a stale read isn't mistaken for fresh.

## Run

```
cd rust && make test
```

Source: [Chase & Lev, *Dynamic Circular Work-Stealing Deque* (SPAA 2005)](https://www.di.ens.fr/~zappa/readings/ppopp13.pdf)
