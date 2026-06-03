# 37 — Fenwick Tree (Binary Indexed Tree)

Maintain an array under point `update(i, delta)` and `sum(i)` prefix queries, both O(log n), over 2·10⁵ mixed queries.
Medium because the structure is unusually terse — one flat array and two bit-twiddling loops — but *why* `i & (-i)` walks the right indices is the non-obvious part.

## Input / Output
```
{"n":<int>,"initial":[…],"queries":[["sum",i] | ["update",i,delta], …]}
---
s1 s2 …    one answer per "sum" query, in order
```

## Teaches

- **Lowest-set-bit traversal**: `update` walks up with `i += i & (-i)`, `sum` walks down with `i -= i & (-i)`; each index stores the sum of a block whose length is its lowest set bit.
- **Why it works**: the index's binary representation partitions `[1, i]` into O(log n) power-of-two blocks; prefix-only and invertible, unlike a segment tree (challenge 22).

## Run
```
cd rust   && make
cd go     && make
cd python && make
```
Source: [CP-Algorithms — Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
