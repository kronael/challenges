# 04 — Chase-Lev Work-Stealing Deque

Owner thread `push`/`pop` at the bottom; any number of thieves `steal` from the
top. The buffer grows when full. Atomics only on the hot path.

The trap is the single-element race. When `bottom - top == 1`, the owner's `pop`
and a thief's `steal` both target the same slot — exactly one may win. The owner
speculatively decrements `bottom`, reads the item, then CASes `top` upward; if
the CAS fails a thief took it, so the owner returns Empty and restores `bottom`.
ABA lurks here: `top` must carry enough state (or the CAS must be strong enough)
that a stale read can't be mistaken for a fresh one.

The ordering trap: that decisive `top` CAS — and the thief's matching `top` CAS —
must be `SeqCst`. The owner's `bottom` store and the thief's `top` load form a
Dekker-style pattern; with anything weaker than `SeqCst` both sides can read the
old value and both claim the last element (duplication).

The test: owner pushes 500k items interleaved with its own pops while 7 thieves
steal concurrently (Barrier-synced start). It verifies the union of owner-popped
and stolen items is exactly the full set — exact **count** and **sum**, so no
item is lost (both sides yielded) or duplicated (both claimed the last one).

`make test` · `make bench` (steal throughput, 7 thieves)
