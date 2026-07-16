# 10 — Medium — Route Costs

**Task**: Compute the shortest distance from node 0 to every other node in a weighted directed graph.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Given a directed graph with non-negative edge weights, output the shortest-path
distance from node `0` to each node, or `-1` for any node you can't reach. The
distance to a node is the minimum total weight over every directed path from
node `0` to it. Multiple directed edges between the same two nodes may appear.

Constraints: `1 <= n <= 10^5`, `0 <= len(edges) <= 5*10^5`, edge endpoints are
valid node ids, weights are non-negative integers, and distances fit in i64.

## Input

```json
{"n": 4, "edges": [[0,1,4],[0,2,1],[2,1,2],[1,3,1]]}
```
Each edge is `[u, v, w]`: a directed edge u → v with weight w.

## Output

`d0 d1 … d(n−1)`, space-separated; `-1` where a node is unreachable.

## Examples

**Example 1** — the direct edge 0→1 costs 4, but detouring 0→2→1 costs only 3
```
{"n":4,"edges":[[0,1,4],[0,2,1],[2,1,2],[1,3,1]]} → 0 3 1 4
```

**Example 2** — node 2 has no incoming path
```
{"n":3,"edges":[[0,1,5]]} → 0 5 -1
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
