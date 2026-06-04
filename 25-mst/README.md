# 25 — Minimum Spanning Tree

**Task**: Find the cheapest set of roads that connects all `n` cities.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

You are given `n` cities and `m` candidate roads. Each road joins two cities and
has a construction cost. Choose a subset of the roads so that every city is
reachable from every other city, and the total construction cost is as small as
possible. Output that minimum total cost.

The graph is connected, so a connecting subset always exists; the minimal one is
a spanning tree (`n − 1` roads). The trap is scale and cycles: with up to
`m = 2·10⁵` candidate roads you cannot afford to recheck the whole partial
network every time you consider adding a road, and any road that closes a loop
must be rejected — detecting that cheaply is the hard part.

Constraints: `n` up to 10⁴, `m` up to 2·10⁵, costs fit in i32, the graph is
connected (a spanning tree exists).

## Input

```json
{"n": 4, "edges": [[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]}
```

`edges[i] = [u, v, w]`: a road between cities `u` and `v` (0-indexed) costing `w`.

## Output

A single integer: the total weight of the minimum spanning tree.

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

Source: CLRS §23 (minimum spanning trees)
