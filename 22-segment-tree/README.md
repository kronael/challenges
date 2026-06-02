# 22 — Segment Tree (Range Sum, Point Update)

Maintain an array under two operations: `["sum",l,r]` returns the sum over the inclusive 1-indexed range `[l,r]`, and `["update",i,v]` sets position `i` to value `v`.

## Input / Output

```
{"n":<int>,"values":[<int>,…],"ops":[["sum",l,r] | ["update",i,v],…]}
---
s1 s2 …      one answer per "sum" op, in order
```

## Examples

```
{"n":5,"values":[1,3,2,5,4],"ops":[["sum",1,3],["update",2,10],["sum",1,5]]}
→ 6 22

{"n":3,"values":[1,2,3],"ops":[["sum",2,3],["update",1,5],["sum",1,1]]}
→ 5 5
```

## Key insight

A segment tree stores partial sums over a balanced binary decomposition of the array, so both a point update and a range query touch only O(log n) nodes.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
