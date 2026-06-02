# 13 — Dijkstra Shortest Path

Given a directed weighted graph with `n` nodes and non-negative edge weights, output the shortest-path distance from node `0` to every node. Unreachable nodes get `-1`.

## Input / Output

```
{"n":<int>,"edges":[[u,v,w],…]}      directed edge u→v with weight w
---
d0 d1 … dn-1      distances from node 0, -1 if unreachable
```

## Examples

```
{"n":4,"edges":[[0,1,4],[0,2,1],[2,1,2],[1,3,1]]}
→ 0 3 1 4

{"n":3,"edges":[[0,1,5]]}
→ 0 5 -1
```

## Key insight

Min-heap Dijkstra: repeatedly pop the closest unsettled node and relax its out-edges, skipping stale heap entries. O((V+E) log V) with non-negative weights.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
