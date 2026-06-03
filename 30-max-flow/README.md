# 30 — Max Flow

Maximum flow from node 1 to node n in a directed graph with integer edge capacities (parallel edges add).
Hard because plain Ford-Fulkerson is O(VE²) and can crawl on adversarial graphs; Dinic's level-graph structure brings it to O(V²·E).

## Input / Output
```
{"n":<int>,"edges":[[u,v,c],…]}      directed edge u→v with capacity c, 1-indexed
---
<int>      maximum flow from node 1 to node n
```

## Teaches

- **Dinic's algorithm**: BFS builds a level graph (shortest-layer distances from the source), then DFS finds a blocking flow along level-respecting edges; repeat until the sink is unreachable.
- **Why O(V²·E) beats O(VE²)**: each phase strictly increases the shortest augmenting-path length, so there are at most V phases.
- **Residual graph**: every edge carries a back-edge so flow can be cancelled.

## Run
```
cd rust   && make
cd go     && make
cd python && make
```
Source: [CSES #1694 — Download Speed](https://cses.fi/problemset/task/1694)
