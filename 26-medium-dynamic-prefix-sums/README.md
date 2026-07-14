# 26 — Medium — Dynamic Prefix Sums

**Task**: Support two operations on an array: add a value to element `i`, and
query the prefix sum up to index `i`.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

You maintain an array `a` of `n` numbers and process a stream of two kinds of
operations, in order:

- `update i d` — add `d` to element `i`.
- `sum i` — report the prefix sum `a[1] + a[2] + … + a[i]`.

Sums can be large: with `n = 2·10⁵` elements and values up to ~`10¹⁸`, a prefix
sum overflows 32 bits, so accumulate in 64-bit integers.

Constraints: `n` up to 2·10⁵, up to 2·10⁵ queries, indices are 1-based.

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

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.
