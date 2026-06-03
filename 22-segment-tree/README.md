# 22 — Segment Tree (Range Sum, Point Update)

Maintain an array under interleaved range-sum queries and point updates, both in O(log n). The challenge is a balanced decomposition that makes every operation touch only a logarithmic slice.

## Input / Output

```
{"n":<int>,"values":[<int>,…],"ops":[["sum",l,r] | ["update",i,v],…]}
---
s1 s2 …      one answer per "sum" op, in order (1-indexed, inclusive)
```

## Example

```
{"n":5,"values":[1,3,2,5,4],"ops":[["sum",1,3],["update",2,10],["sum",1,5]]}
→ 6 22
```

## Teaches

- **Halving the range per level**: each node owns a contiguous span; a query or update splits into O(log n) canonical nodes, so neither costs O(n).
- **Lazy propagation**: the same tree supports *range* updates by deferring a pending delta at a node and pushing it down only when a child is visited — avoiding O(n) per range write.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: https://cses.fi/problemset/
