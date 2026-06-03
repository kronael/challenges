# 22 — Segment Tree

**Task**: Support point updates and range-sum queries on an array, both in O(log n).

**Difficulty**: hard
**Time estimate**: ~50 min

## Problem

Given an array, handle a mix of two operations in any order: update the element at index `i`, and query the sum over a range `[l, r]`. A plain array gives O(1) update but O(n) query; a prefix-sum array gives O(1) query but O(n) update — neither survives when both kinds of op are interleaved heavily. You need *both* in O(log n).

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

## Teaches

- **Halving the range per level**: each node owns a contiguous span; a query or update splits into O(log n) canonical nodes, so neither costs O(n).
- **Lazy propagation**: the same tree supports *range* updates by deferring a pending delta at a node and pushing it down only when a child is visited.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: https://cses.fi/problemset/
