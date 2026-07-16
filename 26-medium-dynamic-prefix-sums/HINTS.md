# Hints — 26 Medium — Fenwick Tree

> Spoilers. Open only when stuck.

- **Fenwick tree (Binary Indexed Tree)**: keep one flat array `tree` of size
  `n+1`, all zeros. It is startlingly terse — two short loops, both driven by the
  lowest set bit of the index. Both `update` and `sum` run in O(log n).
- **Lowest-set-bit traversal**: `i & (-i)` isolates the lowest set bit of `i`.
  `update` walks *up* with `i += i & (-i)` until it passes `n`; `sum` walks *down*
  with `i -= i & (-i)` until it hits 0. Each index stores the sum of a block whose
  length is its lowest set bit.
- **Why it works**: the binary form of `i` partitions `[1, i]` into O(log n)
  power-of-two blocks, and the down-walk visits exactly one stored block per set
  bit. It is prefix-only and invertible — simpler than a full segment tree.
- **Building the initial array**: just call `update(i, a[i])` for each element,
  or fill the tree in O(n) with a direct propagation pass.
- **Range sums** if you need them: `sum(r) - sum(l-1)`. (This problem only asks
  for prefix sums.)

The naive O(n) per-operation approach (rescan the array for every `sum`, or
recompute the prefix array after every `update`) is what `rotten/main.py` does —
correct, but it TIMEOUTs on the large cases.

Source: [CP-Algorithms — Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
