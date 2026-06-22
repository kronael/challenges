# 06 — Lock-Free Stack Reclamation

**Task**: Implement a lock-free stack whose nodes are reclaimed safely. A node
must never be dereferenced after it is removed, and every value that is pushed
must be popped exactly once.

**Difficulty**: expert
**Time estimate**: ~120 min

## Problem

The stack is shared by many threads. Each thread repeatedly pushes and pops while
other threads are changing the same top pointer. Removing a node is not enough:
the implementation must also decide when that node can be returned to the
allocator without racing a thread that already loaded it.

The stress test checks three invariants:

- every pushed value is popped exactly once
- no popped value comes from memory that has already been reclaimed
- all allocated nodes and payloads are released when the stack is dropped

Constraints: 16 concurrent threads in the test, each performing about 10,000
operations. The stack must remain lock-free and must reclaim memory without a
garbage collector.

## Run

```
cd rust && make test
```

Stuck? See `HINTS.md`.

Source: [Maged M. Michael, IEEE TPDS 2004](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf)
