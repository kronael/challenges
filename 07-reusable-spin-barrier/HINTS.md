# Hints — 07 Sense-Reversing Barrier

> Spoilers. Open only when stuck.

- **Why a shared count alone fails**: a single shared count can't distinguish
  phase K from phase K+1. The not-yet-reset count leaks across rounds, so a fast
  thread that loops into the next phase sees the stale value and is released
  early.
- **Use the waiter handle**: the scaffold gives each participant its own state:
  `let mut waiter = barrier.waiter()` in Rust, or
  `waiter := barrier.NewWaiter()` in Go. Keep that waiter private to one
  thread or goroutine and call `wait`/`Wait` on it for every phase.
- **Sense reversal**: give each thread a *local* sense bit (pass it in, or use a
  `thread_local!`), plus one *shared* sense bit. Threads spin on the shared
  sense, never on the count. The last arriver resets the count to N and *flips*
  the shared sense; everyone else spins until `shared_sense != local_sense`,
  then flips their local sense for the next round. A stale count can no longer
  release anyone, because release is gated on the sense flip, not the count.
- **Detecting the last arriver**: `fetch_add` (or `fetch_sub`) the count
  atomically and compare the returned value — the thread that brings the count
  to N (or to 0, if you count down) is the last one and does the reset + flip;
  all others wait on the sense.
- **Ordering**: the count reset must be visible to peers *before* the sense
  flip, or a thread released by the flip could still see the old count. Use a
  release on the sense store (and the count reset under it) paired with an
  acquire on the waiters' sense load — `fetch_add(AcqRel)` on arrival, `Release`
  on the sense flip, `Acquire` on the spin load. Plain `Relaxed` stores do not
  give this guarantee.
- **First round**: initialise the local sense so its first flip lands on a value
  that differs from the initial shared sense — otherwise phase-0 waiters fall
  straight through.

`rotten/main.c` is the trap: it resets the count but never reverses sense (it
re-spins on the count == N condition), so a thread looping into the next phase
sees the stale count and is released early. Correct single-threaded; fails the
multi-phase stress test.

Source: [Mellor-Crummey & Scott, *Algorithms for Scalable Synchronization* (ACM TOCS 1991)](https://www.cs.rochester.edu/u/scott/papers/1991_TOCS_synch.pdf)
