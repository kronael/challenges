# 06 — Hazard-Pointer Treiber Stack

**Task**: Implement a lock-free Treiber stack with hazard-pointer reclamation, so a freed node is never dereferenced by another thread — no GC, no leaks, no use-after-free.

**Difficulty**: expert
**Time estimate**: ~120 min

## Problem

A Treiber stack pushes and pops by CASing `head`. But a CAS compares the pointer,
not its generation: pop A, pop B, push A back, and a stale CAS from A to A's old
`next` succeeds even though that `next` now points at freed memory — the ABA
problem, silently corrupting the stack.

Hazard pointers fix it: before dereferencing a pointer you *publish* it to a
per-thread hazard slot, then *re-validate* that `head` is unchanged; the reclaimer
only frees a node no hazard slot points at. The subtle part is that the
publish-then-validate must use `SeqCst` — `Release`/`Acquire` leaves a TOCTOU
window where a node is freed after publish but before the re-check. The stress
test hammers the stack from many threads and asserts no use-after-free and no lost
nodes.

## Teaches

- **ABA**: `head` CAS from A to A's stale `next` succeeds even though `next` now points at freed memory; hazard pointers fix it with no per-node atomics on the read path.
- **Guess–publish–verify**: load `head` (guess), write it to your hazard slot (publish), re-load `head` and confirm unchanged (verify) before dereferencing.
- **SeqCst between publish and verify**: `Release`/`Acquire` leaves a window where a node is freed after publish but before the re-check; the reclaimer's slot scan must be SeqCst too.

## Run

```
cd rust && make test
```

Source: [Michael, *Hazard Pointers* (IEEE TPDS 2004)](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf)
