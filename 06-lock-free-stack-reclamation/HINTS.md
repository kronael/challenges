# Hints — 06 Hazard-Pointer Treiber Stack

> Spoilers. Open only when stuck.

- **Where the race comes from**: a Treiber stack pushes and pops by
  compare-and-swapping a single `head` pointer. The hard part is reclamation.
  One thread can load `head` and be about to read the node while another thread
  removes that same node and returns it to the allocator.
- **ABA**: a CAS compares the pointer value, not the node's lifetime. If node A
  is popped, node B is popped, and A is later pushed again, a stale CAS from A to
  A's old `next` can succeed even though that `next` no longer belongs to the
  same stack state. The result can be a lost node, a duplicate pop, or a read
  from reclaimed memory.
- **Hazard pointers**: before dereferencing a pointer you *publish* it to a
  per-thread hazard slot, then *re-validate* that `head` is unchanged; the
  reclaimer only ever frees a node that no hazard slot currently points at. This
  needs no per-node atomics on the read path.
- **ABA**: a `head` CAS from A to A's stale `next` succeeds even though `next` now
  points at freed memory. Hazard pointers fix it by keeping any node a thread is
  about to touch unreclaimable until the thread is done.
- **Guess–publish–verify**: load `head` (the guess), write it to your hazard slot
  (publish), then re-load `head` and confirm it is unchanged (verify) before
  dereferencing. If it moved, your guess may already be retired — retry.
- **SeqCst between publish and verify**: `Release`/`Acquire` leaves a window where
  a node is freed after you publish but before you re-check. The store to the
  hazard slot, the fence, the verifying load, and the reclaimer's slot scan must
  all be `SeqCst`, or the TOCTOU window stays open.
- **Retire, don't free**: on a successful pop, the popped node goes onto a
  per-thread retire list rather than being freed immediately. Periodically scan
  the retire list against every hazard slot and free only the nodes no slot
  guards; the rest wait for the next scan.
- **Slot hygiene**: `hazard[tid]` must always name exactly the node this thread is
  currently dereferencing, or be NULL. Clear it on every exit from `pop` that is
  not a successful claim — a stale hazard pins a node forever (leak) or lets the
  thread later trust a slot it no longer guards.

The wrong-but-tempting version frees each popped node immediately (plain Treiber,
no hazard pointers) — correct single-threaded, but under concurrency it
use-after-frees and ABA-corrupts. That is what `rotten/main.c` does.

Source: [Maged M. Michael, IEEE TPDS 2004](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf)
