# 24 — Topological Sort

**Task**: Order tasks so every prerequisite comes before the task that needs it, or report a cycle.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have tasks with prerequisites: task A must complete before task B (a directed edge A→B). Find an ordering that satisfies all prerequisites — like a build system or a course schedule — breaking ties by smallest node number. If a cycle makes any valid ordering impossible, output `CYCLE`. The neat part: cycle detection falls out of the ordering for free.

## Input

```json
{"n": 6, "edges": [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]}
```

## Output

A valid ordering on one line, space-separated, or `CYCLE`.

## Examples

**Example 1** — tie-breaking by smallest ready node makes the order deterministic
```
n=6, edges [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]] → 4 5 2 0 3 1
```

**Example 2** — a mutual prerequisite has no valid order
```
n=2, edges [[0,1],[1,0]] → CYCLE
```

## Teaches

- **Kahn's BFS by in-degree**: repeatedly emit a node with in-degree 0 and decrement its successors; a min-heap of ready nodes yields the lexicographically smallest order.
- **Cycle = leftover nodes**: if fewer than `n` nodes are emitted, the rest form a cycle.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: CLRS §22.4
