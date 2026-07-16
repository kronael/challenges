# 35 — Hard — Dynamic Range Sums

**Task**: Maintain an array under point assignments and inclusive range-sum queries.

**Difficulty**: hard
**Time estimate**: ~50 min

## Problem

Given an array of `n` values, process a sequence of operations of two kinds,
interleaved in any order:

- `update i v` — set the element at index `i` to `v`.
- `sum l r` — report the sum of the elements in the inclusive range `[l, r]`.

Indices are 1-based and ranges are inclusive. Emit one answer per `sum`, in the
order the `sum` operations appear.

Constraints: `n` and the number of operations each up to 2·10⁵; values and the
running sums fit in a 64-bit signed integer.

## Input

```json
{"n": 5, "values": [1,3,2,5,4], "ops": [["sum",1,3],["update",2,10],["sum",1,5]]}
```

## Output

One answer per `"sum"` op, in order, space-separated (1-indexed, inclusive ranges).

## Examples

**Example 1** — an update between two sums changes the second answer
```
values [1,3,2,5,4], [sum 1-3][update 2→10][sum 1-5] → 6 22
```

**Example 2** — a single-element range is just that element
```
values [7,8,9], [sum 2-2] → 8
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

Source: CSES Problem Set — Dynamic Range Sum Queries (https://cses.fi/problemset/task/1648)
