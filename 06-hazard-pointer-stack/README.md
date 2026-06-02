# 06 — Hazard-Pointer Treiber Stack

Lock-free Treiber stack with hazard-pointer reclamation. No GC, no leaks, no
use-after-free.

The ABA trap: `pop` reads `head -> A`, is preempted; another thread pops A, pops
B, pushes A back. Now `pop` CASes `head` from A to A's stale `next` (pointing at
freed B). The CAS succeeds — it checks the pointer, not the generation — and the
stack is corrupt. Per-load refcounting is too slow; hazard pointers fix it with
no per-node atomics on the read path.

Correct approach (guess–publish–verify): load `head` (guess), write it into your
thread's hazard slot (publish), re-load `head` and confirm unchanged (verify)
before dereferencing. A retired node is freed only once no hazard slot points at
it. The fence between publish and verify, and the reclaimer's slot scan, must
both be `SeqCst` — `Release`/`Acquire` opens a TOCTOU window where a node is
freed after a reader published but before it re-checked.

The test: 16 threads each push+pop 10k times on a payload whose `Drop` bumps an
atomic counter; at the end **constructs == drops, live == 0** — leaks (>0),
double-frees (<0). A use-after-free trips the counter or segfaults.

`make test` · `make bench` (push+pop throughput, 16 threads)
