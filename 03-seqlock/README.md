# 03 — Seqlock

**Task**: Guard a 64-byte market-data tick (8 doubles) so that one writer can keep overwriting it while many readers copy it concurrently — and no reader ever observes a torn write.

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

A single writer keeps stamping new ticks into one shared 64-byte slot. Many
reader threads copy that slot, on a hot path, without blocking the writer and
without taking a lock that the writer has to wait on. Reads must be wait-free in
the common case; a reader that collides with a write may retry, but it must
never hand back a value the writer never wrote.

The payload is wider than any atomic, so a reader copying it while the writer
overwrites it can stitch together bytes from two different ticks — a value that
never existed (e.g. the high half of the new tick with the low half of the old
one). Worse, that mid-write read is a genuine data race, which is undefined
behaviour in C/C++/Rust: there is no "read during a race" you can simply
tolerate and then discard.

The trap is memory ordering. An implementation can look correct and pass a
single-threaded check, yet on a weakly-ordered CPU the hardware (or the
compiler) is free to move the payload copy outside the window you thought
guarded it, so a stale or half-updated copy slips through. x86's strong memory
model hides this; ARM and other weak-memory machines expose it. The stress test
runs a writer and many readers and asserts that every observed tick is
internally consistent — across millions of iterations, a single torn read fails
it.

Constraints: exactly one writer thread; up to ~15 concurrent readers; payload
is a fixed 64 bytes; no `Mutex` or OS blocking primitive.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.

Source: [Wikipedia — Seqlock](https://en.wikipedia.org/wiki/Seqlock)
