# 26 — Matrix Chain Multiplication

Given the dimensions of a chain of `k` matrices, find the parenthesization minimizing scalar multiplications. The challenge is that the optimal split of a range depends on optimal splits of its subranges.

## Input / Output

```
{"dims":[<int>,…]}      k+1 dimensions for k matrices (matrix i is dims[i]×dims[i+1])
---
<int>      minimum scalar multiplications
```

## Example

```
{"dims":[10,30,5,60]}
→ 4500      ((A·B)·C beats A·(B·C))
```

## Teaches

- **Interval DP**: `dp[i][j]` is the best cost for matrices `i…j`; solve all length-2 intervals first, then length 3, ... so every split reuses already-solved smaller subproblems.
- **Choosing a split point**: try each `k` in `[i,j)` and combine `dp[i][k] + dp[k+1][j] + dims[i]·dims[k+1]·dims[j+1]` — O(n³) over n²/2 intervals.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: CLRS §15.2
