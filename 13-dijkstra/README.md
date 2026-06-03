# 13 — Dijkstra Shortest Path

**Task**: Compute the shortest distance from node 0 to every other node in a weighted directed graph.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Given a directed graph with non-negative edge weights, output the shortest-path distance from node `0` to each node, or `-1` for any node you can't reach.

The engine is a greedy min-heap: repeatedly settle the closest unfinished node and relax its out-edges. The correctness rests entirely on weights being non-negative — once a node is popped, its distance is final, because no later (longer) path can ever improve it. Hand this algorithm a negative edge and that guarantee collapses: a node can be "settled" too early and the answer goes wrong. (Detecting negatives is Bellman-Ford's job, not this one.)

Constraints: n up to ~10⁵, edges up to ~5·10⁵, weights non-negative, distances fit in i64.

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

## Teaches

- **Greedy shortest paths with a min-heap**: pop the nearest unsettled node, relax its edges; popped = final, which is exactly why negative weights break it.
- **Lazy heap deletion**: push improved distances as fresh entries and skip any pop where `d > dist[u]` — no decrease-key needed.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §24.3
