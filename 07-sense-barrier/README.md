# 07 — Sense-Reversing Barrier

Reusable N-thread barrier built from atomics only — no Mutex, Condvar, or OS
sleep. `wait()` returns only after all N threads have called it this round.

The reuse trap: a naive "spin until count == N, then reset count to 0" barrier
breaks on the very next round. A fast thread can finish round K, loop back, and
see the not-yet-reset count still at N for round K+1 — passing before its peers
arrive. Sense reversal fixes this: each thread keeps a local sense bit; the last
arriver resets the count and flips a shared sense; everyone else spins until the
shared sense flips, then flips their local copy. The flipped bit, not the count,
is the release signal, so a stale count can never leak across rounds.

The ordering trap: `count.store(N, Relaxed); sense.store(new, Release)` does NOT
guarantee other threads see the count reset before the sense flip. A waiter
released by the new sense may still read the old count and miscount the next
round. You need a `fence(Release)` covering both stores (and `Acquire` on the
waiters' sense load), or make the sense store `SeqCst`.

The test: 16 threads run 1M rounds. Around each barrier every thread stamps the
round number into its slot; after the second barrier each verifies **all 16**
slots hold the current round — a thread released early sees a stale slot (caught),
and a stuck thread never arrives so the test hangs to timeout (caught).

`make test` · `make bench` (rounds/sec, 16 threads)
