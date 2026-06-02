# 07 — Sense-Reversing Barrier

Reusable N-thread barrier from atomics only — no Mutex, Condvar, or OS sleep.
`wait()` returns only after all N threads have called it this round.

The reuse trap: a naive "spin until count == N, then reset to 0" barrier breaks
on the next round — a fast thread finishes round K, loops back, and sees the
not-yet-reset count still at N for K+1, passing before its peers arrive. Sense
reversal fixes it: each thread holds a local sense bit; the last arriver resets
the count and flips a shared sense; others spin until the shared sense flips,
then flip their local copy. The flipped bit, not the count, is the release
signal, so a stale count can never leak across rounds.

The ordering trap: `count.store(N, Relaxed); sense.store(new, Release)` does NOT
guarantee peers see the count reset before the sense flip. Use a `fence(Release)`
covering both stores (and `Acquire` on the waiters' load), or `SeqCst` on sense.

The test: 16 threads, 100k rounds; two barriers bracket each round where every
thread stamps the round into its slot, then verifies **all 16** slots hold it.
Early release sees a stale slot (caught); a stuck thread hangs to timeout (caught).

`make test` · `make bench` (rounds/sec, 16 threads)
