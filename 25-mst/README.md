# 25 — Minimum Spanning Tree (Kruskal)

Compute the total weight of a minimum spanning tree of a connected weighted graph. The challenge is proving the greedy choice is safe and detecting cycles cheaply.

## Input / Output

```
{"n":<int>,"edges":[[u,v,w],…]}      undirected edge u–v with weight w
---
<int>      total weight of the MST
```

## Example

```
{"n":4,"edges":[[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]}
→ 19      (edges 5 + 6 + 4 + ... minus the cycle-forming ones)
```

## Teaches

- **Greedy by the cut property**: sort edges ascending and add the cheapest edge that joins two different components; it is always safe to take.
- **DSU for cycle tests**: union-find answers "would this edge create a cycle?" in O(α), making the whole algorithm O(E log E) dominated by the sort.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: CLRS §23
