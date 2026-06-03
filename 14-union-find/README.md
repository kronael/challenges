# 14 — Union-Find (DSU)

Maintain disjoint components over `n` nodes under a stream of merges, then answer connectivity queries. The hard part is making each operation near-constant despite arbitrary merge orders.

## Input / Output

```
{"n":<int>,"unions":[[u,v],…],"queries":[[u,v],…]}
---
q0 q1 …      one value per query: 1 if same component, else 0
```

## Example

```
{"n":5,"unions":[[0,1],[1,2],[3,4]],"queries":[[0,2],[0,3],[3,4]]}
→ 1 0 1
```

## Teaches

- **Amortized O(α(n)) via two tricks together**: path compression flattens trees on `find`, union by rank keeps them shallow; neither alone is enough, but combined they give inverse-Ackermann (effectively constant) per op.
- **Representative-based equivalence**: connectivity reduces to "same root", turning a relation into pointer chasing.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: CLRS §21
