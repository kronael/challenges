# 06 — Hazard-Pointer Treiber Stack

Lock-free Treiber stack with hazard-pointer memory reclamation — no GC, no leaks, no use-after-free.
Hard because a CAS on `head` checks the pointer, not its generation, so an ABA cycle (pop A, pop B, push A) silently corrupts the stack, and reclaiming nodes safely under concurrent readers is a TOCTOU minefield.

## Teaches

- **ABA**: `head` CAS from A to A's stale `next` succeeds even though `next` now points at freed memory; hazard pointers fix it with no per-node atomics on the read path.
- **Guess–publish–verify**: load `head` (guess), write it to your hazard slot (publish), re-load `head` and confirm unchanged (verify) before dereferencing.
- **SeqCst between publish and verify**: `Release`/`Acquire` leaves a window where a node is freed after a reader published but before it re-checked; the reclaimer's slot scan must be SeqCst too.

## Run
```
cd rust && make
```
Source: [Michael, *Hazard Pointers* (IEEE TPDS 2004)](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf)
