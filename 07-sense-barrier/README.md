# 07 — Sense-Reversing Barrier

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

Reuse is the hard part. The naive version — "increment a count, spin until
count == N, then reset" — cannot be reused safely: a fast thread that finishes
a phase and loops straight into the next one can observe the not-yet-reset count
still sitting at N and sail through before its peers from the previous phase
have even left. The barrier must distinguish "everyone arrived this round" from
"the counter happens to read N because last round's value is still there", and
it must do so using atomics only — no Mutex, no Condvar, no OS sleep, no channel.

The stress test runs N threads through many phases and asserts that no thread is
ever released before all N have arrived for the current phase (a thread released
early reads a stale per-phase slot), and that no thread stalls forever.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.

Source: [Mellor-Crummey & Scott, *Algorithms for Scalable Synchronization* (ACM TOCS 1991)](https://www.cs.rochester.edu/u/scott/papers/1991_TOCS_synch.pdf)
