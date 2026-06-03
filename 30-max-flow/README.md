# 30 — Max Flow

**Task**: Find the maximum flow that can be pushed from node 1 to node n through a capacitated network.

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

Think of the edges as water pipes, each with a capacity; you want to push as much
as possible from the source (node 1) to the sink (node n). Equivalently, you are
finding the minimum edge-cut that separates them.

Plain Ford–Fulkerson augments one path at a time and degrades to O(V·E²),
crawling on adversarial graphs (long thin augmenting paths). Dinic's algorithm
layers the residual graph by BFS distance and pushes a *blocking flow* per phase,
reaching O(V²·E).

## Input / Output

```json
{"n": 4, "edges": [[1, 2, 3], [2, 4, 2], [1, 3, 4], [3, 4, 5]]}
```
Directed edge `u → v` with capacity `c`, 1-indexed; parallel edges add. Output a
single integer: the maximum flow from node 1 to node n.

## Examples

**Example 1** — two disjoint paths, each bottlenecked.
```
{"n":4,"edges":[[1,2,3],[2,4,2],[1,3,4],[3,4,5]]} → 6
```
Path 1→2→4 carries 2, path 1→3→4 carries 4.

**Example 2** — parallel edges between the same pair sum.
```
{"n":2,"edges":[[1,2,5],[1,2,7]]} → 12
```

## Teaches

- **Dinic's algorithm**: BFS builds a level graph, DFS pushes a blocking flow along level-respecting edges; repeat until the sink is unreachable.
- **Residual graph**: every edge gets a back-edge so flow can be cancelled and re-routed.
- **Why O(V²·E) beats O(V·E²)**: each phase strictly increases the shortest augmenting-path length, capping phases at V.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [CSES #1694 — Download Speed](https://cses.fi/problemset/task/1694)
