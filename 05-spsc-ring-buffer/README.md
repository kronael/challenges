# 05 — SPSC Ring Buffer

**Task**: Implement a single-producer single-consumer ring buffer that sustains 1B+ messages/second — and find why the obvious correct version is 3–5x too slow.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

One producer owns `tail`, one consumer owns `head`, capacity N is a power of two,
no locks. Correctness here is the easy part. The trap is performance: the naive
layout puts `head` and `tail` in the same cache line, and since the two cores
each write their own index every operation, every write invalidates the other
core's cached copy of that line — *false sharing* — and the two threads serialise
through the cache-coherence protocol.

The fix is to pad each index onto its own cache line. The stress test pushes
billions of messages and the bench measures throughput; the unpadded version is
correct but crawls, the padded one flies.

## Teaches

- **False sharing**: two unrelated variables on one cache line, written by different cores, force a MESI invalidation on every write — the threads serialise even though they touch different data.
- **Padding to separate lines**: `#[repr(align(64))]` plus padding puts each index on its own cache line, killing the invalidation traffic.
- **Full-vs-empty**: free-running monotonic counters masked only on slot access — empty is `head == tail`, full is `head - tail == N` — sidesteps the wrap ambiguity.

## Run

```
cd rust && make test
cd go   && make test
```

Source: [Drepper, *What Every Programmer Should Know About Memory* §6.4 (false sharing)](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)
