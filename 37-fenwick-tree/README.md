# 37 — Fenwick Tree (Binary Indexed Tree)

**Task**: Support two operations on an array — add a value to element i, and query the prefix sum up to index i — both in O(log n).

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

Process a mix of point updates and prefix-sum queries over a large array (2·10⁵
operations). A plain array makes updates O(1) but sums O(n); a prefix-sum array
flips it. You need both logarithmic.

The Fenwick tree is startlingly terse — one flat array, two bit-twiddling loops.
The non-obvious part is *why* `i & (-i)` (the lowest set bit) walks exactly the
right indices: each slot stores the sum of a power-of-two block, and the binary
form of i partitions `[1, i]` into O(log n) such blocks.

## Input / Output

```json
{"n": 8, "initial": [1, 3, 2, 4, 5, 2, 6, 1], "queries": [["sum", 4], ["update", 3, 2], ["sum", 4], ["update", 7, -1], ["sum", 8]]}
```
Indices are 1-based; `update i d` adds d to element i. Output one answer per `sum`
query, space-separated, in order.

## Examples

**Example 1** — an update between two sums shifts the second result.
```
init [1,3,2,4,5,2,6,1]: sum4→10, update(3,+2), sum4→12, update(7,-1), sum8→25
  → 10 12 25
```

**Example 2** — a negative delta zeroes out an element.
```
init [5,5,5]: sum3→15, update(1,-5), sum1→0, sum3→10
  → 15 0 10
```

## Teaches

- **Lowest-set-bit traversal**: `update` walks up with `i += i & (-i)`, `sum` walks down with `i -= i & (-i)`; each index stores the sum of a block whose length is its lowest set bit.
- **Why it works**: the binary form of i partitions `[1, i]` into O(log n) power-of-two blocks. Prefix-only and invertible — simpler than a segment tree (challenge 22).

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [CP-Algorithms — Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
