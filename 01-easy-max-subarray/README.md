# 01 — Easy — Maximum Subarray

**Task**: Find the contiguous subarray with the largest sum.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Find the contiguous, non-empty subarray with the largest sum. The subarray must
contain at least one element.

Constraints: `1 <= n <= 10⁶`; values and sums fit in signed 64-bit integers.

## Input

A JSON object with one field:

- `arr`: a non-empty list of integers.

```json
{"arr": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}
```

## Output

A single integer: the maximum contiguous subarray sum.

## Examples

**Example 1** — mixed positive and negative values
```
arr [-2,1,-3,4,-1,2,1,-5,4] → 6   (subarray [4,-1,2,1])
```

**Example 2** — all negative values
```
arr [-5,-2,-8] → -2
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
