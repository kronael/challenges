# 37 — Fenwick Tree (Binary Indexed Tree)

Maintain an array of `n` integers under a mix of two operations:

- `["update", i, delta]` — add `delta` to the element at position `i` (1-indexed).
- `["sum", i]` — return the prefix sum of elements `1..i` (inclusive).

Output the answer to every `sum` query, in order. A naive prefix sum is O(n)
per query; the Fenwick tree makes both operations O(log n), so 2·10⁵ mixed
queries over a 2·10⁵-element array stay fast.

## Input / Output

```
{"n":<int>,"initial":[<int>,…],"queries":[["sum",i] | ["update",i,delta],…]}
---
s1 s2 …      one answer per "sum" query, in order
```

## Examples

```
{"n":8,"initial":[1,3,2,4,5,2,6,1],"queries":[["sum",4],["update",3,2],["sum",4],["update",7,-1],["sum",8]]}
→ 10 12 25

{"n":3,"initial":[5,5,5],"queries":[["sum",3],["update",1,-5],["sum",1],["sum",3]]}
→ 15 0 10
```

## Key insight

A Fenwick tree stores, at each index `i`, the sum of a contiguous block of the
array ending at `i`. The block length is the **lowest set bit** of `i`, computed
as `i & (-i)` in two's complement. To walk the structure:

- `update(i, delta)`: add `delta`, then `i += i & (-i)` to step to the next
  index whose block covers `i` — walking *up* toward the root.
- `prefix_sum(i)`: accumulate `tree[i]`, then `i -= i & (-i)` to drop the last
  block — walking *down* toward zero.

Both loops run in O(log n) because each step clears or adds one bit.

### Fenwick vs. segment tree (challenge 22)

A segment tree (challenge 22) answers an **arbitrary range** `[l, r]` directly
and supports many associative combines (min, max, gcd…). A Fenwick tree answers
only **prefix** queries `[1, i]`; a range sum `[l, r]` must be derived as
`prefix(r) - prefix(l-1)`, which works for sum but not for non-invertible
operations like min. In exchange the Fenwick tree is far smaller: one flat array
of `n+1` longs and two tight loops, with no recursion and roughly half the
constant factor. Reach for it when you only need invertible prefix aggregates.

## Constraints

- `1 ≤ n ≤ 10⁵` (large case: 2·10⁵)
- `1 ≤ q ≤ 10⁵` (large case: 2·10⁵)
- values and partial sums fit in `i64`

## Run

```
cd python && make test && make bench
cd go     && make test && make bench
cd rust   && make test && make bench
```

Source: [CP-Algorithms — Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.
