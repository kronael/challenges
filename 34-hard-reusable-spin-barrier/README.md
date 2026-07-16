# 34 — Hard — Reusable Spin Barrier

**Task**: Implement a reusable N-thread spin barrier from atomics only — no Mutex, Condvar, or OS sleep — that works correctly across many phases.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

A barrier blocks each thread until all N have arrived, then releases them
together, and must work for many successive phases — the same barrier object is
reused round after round.

The Rust and Go scaffolds model each logical participant with its own waiter
handle. Create one waiter per thread or goroutine, then call `wait` or `Wait`
on that same handle in every phase. Sharing one waiter between participants is
outside the contract.

The stress test runs N threads through many phases and asserts that no thread is
released before all N have arrived for the current phase or stalls forever.

## Run

```
make -C rust test
make -C go test
```

Stuck? See `HINTS.md`.
