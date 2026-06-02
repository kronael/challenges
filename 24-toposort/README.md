# 24 — Topological Sort

Given a directed graph on `n` nodes (`0…n-1`), output a topological ordering: every edge `u→v` has `u` before `v`. If the graph has a cycle, output `CYCLE`. Ties are broken by smallest node first, so the answer is unique.

## Input / Output

```
{"n":<int>,"edges":[[u,v],…]}      directed edge u→v
---
o1 o2 … on      a valid ordering, or `CYCLE`
```

## Examples

```
{"n":6,"edges":[[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]}
→ 4 5 2 0 3 1

{"n":2,"edges":[[0,1],[1,0]]}
→ CYCLE
```

## Key insight

Kahn's algorithm: repeatedly remove a node with in-degree 0 (a min-heap gives the lexicographically smallest order) and decrement its neighbors. If fewer than `n` nodes come out, a cycle remains.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
