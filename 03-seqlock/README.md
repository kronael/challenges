# 03 — Seqlock

**Task**: Implement a seqlock guarding a 64-byte market-data tick (8 doubles): one writer, many wait-free readers, and no reader may ever observe a torn write.

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

The payload is wider than any atomic, so a reader copying it while the writer
overwrites it can stitch together bytes from two epochs — a value that never
existed. Worse, that mid-write read is a genuine data race, which is undefined
behaviour in C++/Rust: there is no "read during a race" you can simply tolerate.

The seqlock turns the race into a *retry* using an odd/even sequence counter, but
the read must still be properly ordered or the CPU hoists the load out of the
guarded window. The fence placement that makes this safe on x86 (TSO hides the
bug) is *not* enough on ARM — get the fences right for weak memory. The stress
test runs a writer and many readers and asserts every observed tick is internally
consistent.

## Teaches

- **Torn reads / speculative-read UB**: reading the payload while the writer copies it is a data race; the seq protocol turns it into a retry, but the read must still be ordered.
- **Odd/even seq protocol**: writer does `seq++` (odd) → copy → `seq++` (even); reader checks even-before, copies, re-reads seq, retries on odd-or-changed.
- **Fence placement**: `fence(Acquire)` after the copy + `Release` on the trailing `seq++` stop the CPU hoisting the load. TSO hides the bug on x86; ARM exposes it.

## Run

```
cd rust && make test
cd go   && make test
```

Source: [Wikipedia — Seqlock](https://en.wikipedia.org/wiki/Seqlock)
