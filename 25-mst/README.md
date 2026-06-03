# 25 — Minimum Spanning Tree

**Task**: Find the cheapest set of roads that connects all N cities.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

Connect N cities with M candidate roads, each with a construction cost. Find the minimum total cost to connect every city (build a spanning tree). Unlike coin change, greedy works here — sort edges cheapest-first and take each one that joins two not-yet-connected components. An exchange argument proves it's always safe; the only catch is detecting cycles cheaply.

## Input

```json
{"n": 4, "edges": [[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]}
```

## Output

A single integer: the total weight of the minimum spanning tree.

## Examples

**Example 1** — greedy skips the two costliest edges that would form cycles
```
n=4, edges above → 19   (take 4 + 5 + ... not 10, 15)
```

**Example 2** — already a tree, so every edge is forced
```
n=3, edges [[0,1,2],[1,2,3]] → 5
```

## Teaches

- **Greedy by the cut property**: add the cheapest edge that joins two different components; it is always safe to take.
- **DSU for cycle tests**: union-find answers "would this edge create a cycle?" in O(α), making the algorithm O(E log E), dominated by the sort.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: CLRS §23
