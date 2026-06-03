# 17 — Maximum Subarray

**Task**: Find the contiguous subarray with the largest sum.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Find the contiguous, non-empty subarray with the largest sum. The array can hold negative numbers, so taking everything isn't always best — sometimes the best run sits in the middle, flanked by losses you must skip. Do it in one pass and O(1) memory.

## Input

```json
{"arr": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}
```

## Output

A single integer: the maximum contiguous subarray sum.

## Examples

**Example 1** — the answer skips the leading and trailing negatives
```
arr [-2,1,-3,4,-1,2,1,-5,4] → 6   (subarray [4,-1,2,1])
```

**Example 2** — all negative, so the best is the single least-bad element
```
arr [-5,-2,-8] → -2
```

## Teaches

- **DP with a "best ending here" state**: `cur = max(x, cur + x)` decides whether to extend the previous run or restart; the global best tracks the max over all endings.
- **Online, single-pass**: the recurrence depends only on the prior step, so it streams in O(n) time and O(1) space.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: CLRS §4.1
