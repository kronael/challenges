# 24 — Topological Sort

Order the nodes of a directed graph so every edge points forward, breaking ties by smallest node; output `CYCLE` if no ordering exists. The challenge is detecting a cycle as a side effect of the ordering.

## Input / Output

```
{"n":<int>,"edges":[[u,v],…]}      directed edge u→v
---
o1 o2 … on      a valid ordering, or `CYCLE`
```

## Example

```
{"n":6,"edges":[[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]}
→ 4 5 2 0 3 1
```

## Teaches

- **Kahn's BFS by in-degree**: repeatedly emit a node with in-degree 0 and decrement its successors; a min-heap of ready nodes yields the lexicographically smallest order.
- **Cycle = leftover nodes**: if fewer than `n` nodes are emitted, the rest form a cycle — cycle detection falls out for free.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: CLRS §22.4
