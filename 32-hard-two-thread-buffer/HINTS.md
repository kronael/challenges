# Hints — 32 Hard — SPSC Ring Buffer

> Spoilers. Open only when stuck.

- **The fix is padding**: the naive layout puts `head` and `tail` in the same
  cache line. Since the two cores each write their own index every operation,
  every write invalidates the other core's cached copy of that line — *false
  sharing* — and the two threads serialise through the cache-coherence protocol.
  Pad each index onto its own cache line and the contention disappears.
- **False sharing**: two unrelated variables on one cache line, written by
  different cores, force a MESI invalidation on every write — the threads
  serialise even though they touch different data.
- **Padding to separate lines**: `#[repr(align(64))]` plus padding (or
  `_Alignas(64)` in C) puts each index on its own cache line, killing the
  invalidation traffic.
- **Full-vs-empty**: free-running monotonic counters masked only on slot access
  — empty is `head == tail`, full is `tail - head == N` — sidesteps the wrap
  ambiguity. Mask with `index & (N - 1)` only when indexing a slot.
- **Memory ordering**: the producer stores `tail` with Release after writing the
  slot; the consumer loads `tail` with Acquire before reading the slot (and the
  mirror for `head`). Relaxed loads suffice for an index a thread owns and reads
  back itself. No `SeqCst` is needed.

The slow-but-correct version is the one in `rotten/main.c`: head and tail share a
cache line, so it passes a single-threaded check but runs 3–5x slower than the
padded version under the two-thread bench.

Source: [Drepper, *What Every Programmer Should Know About Memory*](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)
