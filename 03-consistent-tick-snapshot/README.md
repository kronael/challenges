# 03 — Consistent Tick Snapshot

**Task**: Guard a 64-byte market-data tick (8 doubles) so that one writer can keep overwriting it while many readers copy it concurrently — and no reader ever observes a torn write.

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

A single writer keeps stamping new ticks into one shared 64-byte slot. Many
reader threads copy that slot, on a hot path, without blocking the writer and
without taking a lock that the writer has to wait on. Reads must be wait-free in
the common case; a reader that collides with a write may retry, but it must
never hand back a value the writer never wrote.

The payload is wider than any single machine word, so a reader copying it while
the writer overwrites it can stitch together bytes from two different ticks — a
value that never existed. In this challenge, every valid tick stores the same
counter value in all eight 8-byte lanes. The stress test runs a writer and many
readers, then rejects any read where the lanes disagree. Across millions of
iterations, a single mixed snapshot fails the test.

Constraints: exactly one writer thread; up to ~15 concurrent readers; payload
is a fixed 64 bytes; no `Mutex` or OS blocking primitive.

## Run

```
cd rust && make test
cd go   && make test
```

Stuck? See `HINTS.md`.
