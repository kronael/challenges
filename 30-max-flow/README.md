# 30 — Max Flow

**Task**: Find the maximum flow that can be pushed from node 1 to node n through a capacitated network.

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

Think of the edges as water pipes, each with a capacity; you want to push as much
as possible from the source (node 1) to the sink (node n). Equivalently, you are
finding the minimum edge-cut that separates them.

The naive approach — find any one path with spare capacity, push flow along it,
repeat — is correct but degrades badly on adversarial graphs: long thin
augmenting paths make it crawl, and on the large cases it will not finish in
time. Part of the challenge is pushing flow in a way that the number of rounds
stays bounded regardless of how the capacities are chosen.

Constraints: up to `n = 500` nodes; capacities fit in a 64-bit integer and the
total flow can too.

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

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: [CSES #1694 — Download Speed](https://cses.fi/problemset/task/1694)
