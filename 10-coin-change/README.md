# 10 — Coin Change

Given coin denominations (unlimited supply of each) and a target `amount`, find the minimum number of coins that sum exactly to `amount`, or `-1` if it cannot be made.

## Input / Output

```
{"amount":<int>,"coins":[<int>,…]}
---
<count>      min coins, or -1 if impossible
```

## Examples

```
{"amount":11,"coins":[1,2,5]}
→ 3

{"amount":3,"coins":[2]}
→ -1
```

## Key insight

Unbounded-knapsack DP: `dp[a] = 1 + min over coins c of dp[a-c]`. Iterating amounts 0..amount over all coins gives O(amount · #coins).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
