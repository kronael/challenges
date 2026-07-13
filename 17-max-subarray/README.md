# 17 — Maximum Subarray

**Task**: Find the contiguous subarray with the largest sum.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Find the contiguous, non-empty subarray with the largest sum. The array can hold
negative numbers, so taking everything isn't always best — sometimes the best run
sits in the middle, flanked by losses you must skip, and sometimes every element is
negative so the answer is a single least-bad value.

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

**Example 1** — the answer skips the leading and trailing negatives
```
arr [-2,1,-3,4,-1,2,1,-5,4] → 6   (subarray [4,-1,2,1])
```

**Example 2** — all negative, so the best is the single least-bad element
```
arr [-5,-2,-8] → -2
```

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.
