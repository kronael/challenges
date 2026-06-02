# 30 — Max Flow (CSES #1694)

Given a directed graph on `n` nodes (1-indexed) with integer edge capacities, find the maximum flow from node `1` to node `n`. Parallel edges add their capacities.

## Input / Output

```
{"n":<int>,"edges":[[u,v,c],…]}      directed edge u→v with capacity c
---
<int>      maximum flow from node 1 to node n
```

## Examples

```
{"n":4,"edges":[[1,2,3],[2,4,2],[1,3,4],[3,4,5]]}
→ 6

{"n":2,"edges":[[1,2,5],[1,2,7]]}
→ 12
```

## Key insight

Dinic's algorithm: repeatedly BFS to build a level graph (shortest layers from the source), then DFS blocking flows along level-respecting edges. Each phase strictly increases the shortest augmenting path length, giving O(V²·E).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```

Source: [cses.fi/problemset/task/1694](https://cses.fi/problemset/task/1694)
