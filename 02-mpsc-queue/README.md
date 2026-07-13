# 02 — Multi-Producer Queue

**Task**: Implement a lock-free multi-producer single-consumer queue where `push` finishes in bounded steps and `try_pop` has distinct empty and retry results.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

Any number of threads may call `push` simultaneously; exactly one thread calls
`try_pop`. A pop returns an item, `Empty`, or `Retry`. `Empty` means that no item
is queued or being enqueued. `Retry` means the caller should try again.

`push` must finish in bounded steps without blocking, regardless of contention.
The stress test asserts that every pushed message is popped exactly once.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.
