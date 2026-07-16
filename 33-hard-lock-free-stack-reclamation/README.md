# 33 — Hard — Lock-Free Stack Reclamation

**Task**: Implement a lock-free stack whose nodes are reclaimed safely. A node
must never be dereferenced after it is removed, and every value that is pushed
must be popped exactly once.

**Difficulty**: hard
**Time estimate**: ~120 min

## Problem

The stack is shared by many threads. Each thread repeatedly pushes and pops while
other threads are changing the same top pointer. Removing a node is not enough:
the implementation must also decide when that node can be returned to the
allocator without racing a thread that already loaded it.

The stress test checks three observable invariants:

- every pushed value is popped exactly once
- every constructed payload is dropped exactly once
- no payload remains live after the stack is dropped

These checks catch loss, duplication, double drops, and leaks. Ordinary
`cargo test` does not by itself prove that no transient invalid memory access
occurred.

Constraints: 16 concurrent threads in the test, each performing about 10,000
operations. The stack must remain lock-free and must reclaim memory without a
garbage collector.

## Run

```
make -C rust test
```

Stuck? See `HINTS.md`.
