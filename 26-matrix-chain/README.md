# 26 — Matrix Chain Multiplication

`dims` of length `k+1` describes a chain of `k` matrices, where matrix `i` has shape `dims[i] × dims[i+1]`. Find the minimum number of scalar multiplications needed to compute the product, choosing the best parenthesization.

## Input / Output

```
{"dims":[<int>,…]}      k+1 dimensions for k matrices
---
<int>      minimum scalar multiplications
```

## Examples

```
{"dims":[10,30,5,60]}
→ 4500

{"dims":[10,20]}
→ 0
```

## Key insight

Interval DP: `dp[i][j]` = best cost to multiply matrices `i…j`. Try every split point `k`, cost = `dp[i][k] + dp[k+1][j] + dims[i]·dims[k+1]·dims[j+1]`. O(n³).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
