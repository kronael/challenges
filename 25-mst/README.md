# 25 — Minimum Spanning Tree (Kruskal)

Given a connected undirected weighted graph on `n` nodes (`0…n-1`), output the total weight of a minimum spanning tree.

## Input / Output

```
{"n":<int>,"edges":[[u,v,w],…]}      undirected edge u–v with weight w
---
<int>      total weight of the MST
```

## Examples

```
{"n":4,"edges":[[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]}
→ 19

{"n":2,"edges":[[0,1,7]]}
→ 7
```

## Key insight

Kruskal: sort edges by weight and add each edge whose endpoints lie in different components, merging them with union-find. The greedy choice is safe by the cut property. O(E log E).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
