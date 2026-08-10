# Hints — 30 Hard — Seqlock

> Spoilers. Open only when stuck.

- **Torn reads / speculative-read UB**: reading the payload while the writer
  copies it is a data race; you cannot just read it and check afterwards — the
  race itself is UB. The seqlock protocol turns the race into a *retry*, but the
  read must still be properly ordered or the CPU hoists the load out of the
  guarded window.
- **Odd/even seq protocol**: keep a sequence counter. The writer does `seq++`
  (now odd) → copy the payload → `seq++` (now even). A reader reads `seq` first;
  if it is odd a write is in progress, so retry. Otherwise it copies the payload,
  re-reads `seq`, and retries if the second read is odd or differs from the
  first. An unchanged even seq across the copy means no write overlapped it.
- **Fence placement (the hard part)**: a `fence(Acquire)` after the payload copy
  plus `Release` on the trailing `seq++` is what stops the CPU (or compiler)
  hoisting the payload load out of the guarded window. The writer's leading
  `seq++` is also `Release` so the copy cannot float before it. Do NOT reach for
  `SeqCst` unless you can justify it — acquire/release is sufficient and faster.
- **Why x86 lies to you**: x86 is TSO (total store order), so it hides the
  missing fences and a fence-free version passes there. ARM and other
  weak-memory machines reorder freely and expose the bug — which is why the
  ordering must be explicit, not relied on from observed x86 behaviour.

- **A note on strict conformance**: the classic seqlock `memcpy`s a *non-atomic*
  payload while a reader may `memcpy` it concurrently. Under the C11 abstract
  machine that is still a data race — the sequence counter turns it into a retry
  in practice but does not legalize it formally. This is the textbook seqlock and
  is what real hardware runs; a strictly-conforming variant would make the payload
  slots `_Atomic` and load/store them `memory_order_relaxed` inside the guarded
  window. The reference keeps the textbook form deliberately; the fences, not the
  payload type, are the point of the exercise.

The wrong-but-tempting version (`rotten/main.c`) just `memcpy`s the payload with
no sequence counter and no fence. It passes a single-threaded check but tears
under a concurrent writer.

Source: [Wikipedia — Seqlock](https://en.wikipedia.org/wiki/Seqlock)
