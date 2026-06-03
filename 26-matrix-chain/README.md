# 26 — Matrix Chain Multiplication

**Task**: Find the parenthesization of a matrix product that minimises scalar multiplications.

**Difficulty**: hard
**Time estimate**: ~50 min

## Problem

You need to multiply a chain of K matrices. The order doesn't change the result, but it dramatically changes how many scalar multiplications it costs — a good split and a bad split can differ by orders of magnitude. Given the dimensions, find the cheapest order. The challenge: the best split of a range depends on the best splits of its subranges.

## Input

```json
{"dims": [10, 30, 5, 60]}
```

`k+1` dimensions for `k` matrices; matrix `i` is `dims[i] × dims[i+1]`.

## Output

A single integer: the minimum number of scalar multiplications.

## Examples

**Example 1** — the two orders differ hugely
```
dims [10,30,5,60] → 4500   (A·B)·C costs 4500 vs A·(B·C) at 27000
```

**Example 2** — two matrices, only one order
```
dims [5,10,20] → 1000
```

## Teaches

- **Interval DP**: `dp[i][j]` is the best cost for matrices `i…j`; solve length-2 intervals first, then length 3, ... so every split reuses solved subproblems.
- **Choosing a split point**: try each `k` in `[i,j)` and combine `dp[i][k] + dp[k+1][j] + dims[i]·dims[k+1]·dims[j+1]` — O(n³) over n²/2 intervals.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: CLRS §15.2
