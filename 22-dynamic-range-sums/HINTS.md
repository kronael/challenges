# Hints — 22 Segment Tree

> Spoilers. Open only when stuck.

- **Segment tree**: build a balanced binary tree over the array where each node
  owns a contiguous span and stores the sum of that span. Then both operations
  touch only O(log n) nodes.
- **Halving the range per level**: a `sum l r` query splits into O(log n)
  canonical nodes whose spans tile `[l, r]` exactly, and a point `update` walks
  the single root-to-leaf path fixing each ancestor's sum — so neither costs
  O(n).
- **Iterative (bottom-up) variant**: a flat array of size `2·size` (`size` the
  next power of two ≥ `n`) holds the tree; leaves at `size + i`, internal node
  `i` is the sum of children `2i` and `2i+1`. `update` reassigns a leaf and
  re-sums its ancestors; `query` climbs from both ends, adding any node that
  sits on the boundary. No recursion, very cache-friendly.
- **A Fenwick / binary indexed tree** is an alternative for this exact problem
  (point update + prefix sum): O(log n) per op with less code, summing a range
  as `prefix(r) - prefix(l-1)`.
- **64-bit accumulator**: the running sums exceed 32 bits at this scale, so keep
  the totals in a 64-bit signed integer.

The naive approaches — re-scanning the range on every `sum`, or rebuilding a
prefix-sum array on every `update` — are O(n) per operation. That is what
`rotten/main.py` does (correct on the small cases) and it TIMEOUTs on the large
ones, which is the wall this challenge sets.
