# 01 — Vertex Load Assignment

**Task**: Assign bandwidth to every node in a network so adjacent nodes differ by at most 1, matching the fixed nodes and minimising the total.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You're provisioning a network. Adjacent nodes share a link, so their bandwidth may differ by at most 1. A few nodes have a fixed requirement; the rest (`null`) are yours to set. Assign non-negative loads to the free nodes so the constraint holds everywhere and the sum is as small as possible.

The catch: a node 3 hops from a node fixed at 10 can be no lower than 7 — every fixed node forces a lower bound that fades by 1 per hop. Sounds like a distance problem, doesn't it?

Constraints: graph is usually a tree, n up to a few thousand, loads fit in i64.

## Input

```json
{"n": 4, "edges": [[0,1],[1,2],[2,3]], "loads": [10, null, null, null]}
```
`loads[i]` is the fixed value or `null` if free.

## Output

The assigned loads, space-separated on one line.

## Examples

**Example 1** — one anchor, the bound decays one step per hop and never floors out
```
{"n":4,"edges":[[0,1],[1,2],[2,3]],"loads":[10,null,null,null]} → 10 9 8 7
```

**Example 2** — two anchors fight; each node takes the tightest bound, not the nearest
```
{"n":3,"edges":[[0,1],[1,2]],"loads":[5,null,8]} → 5 7 8
```

## Teaches

- **Multi-source propagation**: each fixed node spreads a lower bound `L − dist`; the answer is the pointwise maximum over all sources, floored at 0.
- **BFS as Dijkstra**: unit edges make this a multi-source BFS — the same skeleton that scales to weighted graphs.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: original
