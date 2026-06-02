# 04 — Chase-Lev Work-Stealing Deque

Owner `push`/`pop` at the bottom; any number of thieves `steal` from the top.
The buffer grows when full. Atomics only on the hot path. The trap is the
single-element race. When `bottom - top == 1`, the owner's `pop`
and a thief's `steal` target the same slot — exactly one may win. The owner
speculatively decrements `bottom`, reads the item, then CASes `top` upward; on
CAS failure a thief took it, so the owner returns Empty and restores `bottom`.
ABA lurks: `top` must carry enough state that a stale read isn't mistaken for fresh.

The ordering trap: the decisive `top` CAS (owner) and the matching `top` CAS
(thief) must be `SeqCst`. The owner's `bottom` store and the thief's `top` load
form a Dekker-style pattern; anything weaker lets both read the old value and
both claim the last element (duplication).

The test: owner pushes 500k items interleaved with its own pops while 7 thieves
steal (Barrier-synced). The union of owner-popped and stolen items must be the
full set exactly once each — a repeat means the last-element race was lost, a gap
means an item was dropped. `make test` · `make bench` (steal throughput)
