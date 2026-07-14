# 19 — Medium — Cheapest Road Network

**Task**: Find the cheapest set of roads that connects all `n` cities.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

You are given `n` cities and `m` candidate roads. Each road joins two cities and
has a construction cost. Choose a subset of the roads so that every city is
reachable from every other city, and the total construction cost is as small as
possible. Output that minimum total cost.

Constraints: `n` up to 10⁴, `m` up to 2·10⁵, costs fit in i32, the graph is
connected.

## Input

```json
{"n": 4, "edges": [[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]}
```

`edges[i] = [u, v, w]`: a road between cities `u` and `v` (0-indexed) costing `w`.

## Output

A single integer: the minimum total construction cost.

## Examples

**Example 1** — two of the five roads are left out
```
{"n":4,"edges":[[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]} → 19
```

**Example 2** — already a tree, so every road is forced
```
{"n":3,"edges":[[0,1,2],[1,2,3]]} → 5
```

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.
