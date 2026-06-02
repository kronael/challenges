# 14 — Union-Find (DSU)

Start with `n` singleton nodes `0..n-1`. Apply the given `unions` (merge two components), then answer each query `[u,v]`: are `u` and `v` in the same component?

## Input / Output

```
{"n":<int>,"unions":[[u,v],…],"queries":[[u,v],…]}
---
q0 q1 …      one value per query: 1 if same component, else 0
```

## Examples

```
{"n":5,"unions":[[0,1],[1,2],[3,4]],"queries":[[0,2],[0,3],[3,4]]}
→ 1 0 1

{"n":3,"unions":[],"queries":[[0,1],[2,2]]}
→ 0 1
```

## Key insight

Disjoint-set union with path compression and union by rank gives near-constant amortized (inverse-Ackermann) time per operation.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
