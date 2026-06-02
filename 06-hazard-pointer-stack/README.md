# 06 — Hazard-Pointer Treiber Stack

Lock-free Treiber stack with hazard-pointer reclamation. No GC, no leaks, and no
use-after-free.

The ABA trap: `pop` reads `head -> A`, gets preempted. Another thread pops A,
pops B, pushes A back. Now `pop` CASes `head` from A to A's stale `next` (which
points at freed B). The CAS succeeds — it only checks the pointer, not the
generation — and the stack is corrupt. Reference counting on every load is too
slow; hazard pointers solve it without per-node atomics on the read path.

Correct approach (guess–publish–verify): load `head` (guess), write that address
into your thread's hazard slot (publish), then re-load `head` and confirm it is
unchanged (verify) before dereferencing. On retirement, a node is freed only
once no hazard slot points at it; otherwise it is parked on a retired list.

The ordering trap: the fence between publish and verify must be `SeqCst`, and the
reclaimer's scan of the hazard slots must also be `SeqCst`. With `Release`/`Acquire`
the publish and the reclaimer's load can be reordered, opening a TOCTOU window
where a node is freed after a reader published but before the reader re-checked.

The test: 16 threads each push+pop 10k times on a payload whose `Drop` bumps an
atomic counter. At the end it asserts **allocated == dropped exactly once** —
zero leaks and zero double-frees. A use-after-free trips the counter or segfaults.

`make test` · `make bench` (push+pop throughput, 16 threads)
