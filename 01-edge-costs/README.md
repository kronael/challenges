# 01 — Vertex Load Assignment

A graph (usually a tree) has integer vertex loads, some missing; adjacent loads may differ by at most 1. Assign non-negative loads to the missing vertices so the total is minimised. The trick: a missing vertex's minimum is the largest lower bound any known vertex forces on it — a shortest-distance question in disguise.

**Difficulty: medium** — one non-trivial idea (reframing the constraint as multi-source propagation), solvable in ~30 min.

## Input / Output

```
{"n":<int>,"edges":[[u,v],…],"loads":[<int|null>,…]}
---
l0 l1 … ln-1      assigned loads, space-separated
```

## Example

```
{"n":4,"edges":[[0,1],[1,2],[2,3]],"loads":[10,null,null,null]}
→ 10 9 8 7      a node d hops from load L must be ≥ L-d; max over sources, floored at 0
```

## Teaches

- **Multi-source max-propagation**: each fixed vertex propagates a lower bound `L - dist` outward; the answer is the pointwise maximum of these fronts.
- **BFS/Dijkstra on graphs**: unit-weight edges make this a multi-source BFS; the same skeleton generalises to weighted Dijkstra.
- **JSON parsing**: reading a structured graph (`n`, `edges`, nullable `loads`) into typed input rather than splitting lines.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: original
