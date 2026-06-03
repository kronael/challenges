# 03 — Seqlock

One writer, many wait-free readers, guarding a 64-byte payload with a sequence counter.
Hard because the payload is wider than any atomic, so a reader can stitch together bytes from two different epochs — a value that never existed — and reading mid-write is a genuine data race that is UB in C++.

## Teaches

- **Torn reads / speculative-read UB**: reading the payload while the writer copies it is a data race; the seq protocol turns it into a *retry*, but the read must still be ordered.
- **Odd/even seq protocol**: writer does `seq++` (odd) → copy → `seq++` (even); reader checks even-before, copies, re-reads seq, retries on odd-or-changed.
- **Fence placement**: `fence(Acquire)` after the copy + `Release` on the trailing `seq++` stops the CPU hoisting the load outside the guarded window. TSO hides the bug on x86; ARM exposes it.

## Run
```
cd rust && make
cd go   && make
```
Source: [Wikipedia — Seqlock](https://en.wikipedia.org/wiki/Seqlock)
