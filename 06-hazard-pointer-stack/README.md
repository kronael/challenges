# 06 — Hazard-Pointer Treiber Stack

**Task**: Implement a lock-free Treiber stack whose nodes are reclaimed safely, so a freed node is never dereferenced by another thread — no garbage collector, no leaks, no use-after-free.

**Difficulty**: expert
**Time estimate**: ~120 min

## Problem

A Treiber stack pushes and pops by compare-and-swapping a single `head` pointer.
Concurrency makes reclamation the hard part: the moment one thread pops a node
and frees it, another thread may still be holding that same pointer, loaded an
instant earlier, and about to dereference it.

A CAS compares the pointer value, not its generation, which opens the ABA trap:
pop node A, pop node B, push A back, and a stale CAS that swaps `head` from A to
A's *old* `next` succeeds — even though that `next` was freed in the meantime and
now points at reclaimed memory. The stack is silently corrupted, a node is lost
or double-freed, and a reader can dereference memory that has already been handed
back to the allocator.

The stress test hammers the stack from many threads, each interleaving pushes and
pops, and asserts three invariants: every pushed value is popped exactly once (no
loss, no duplication), no popped node carries poisoned/reclaimed contents (no
use-after-free), and total allocations equal total frees at the end (no leak, no
double-free). A solution that frees a node the instant it is popped passes a
single-threaded run and fails this.

Constraints: many concurrent threads (16 in the test), each performing ~10⁴
push/pop operations; the stack must be lock-free and reclaim memory without a GC.

## Run

```
cd rust && make test
```

Stuck? See `HINTS.md`.

Source: [Michael, *Hazard Pointers* (IEEE TPDS 2004)](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf)
