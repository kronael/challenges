# 10 — Coin Change

Given coin denominations (unlimited supply of each) and a target `amount`, find the minimum number of coins summing exactly to `amount`, or `-1` if impossible. The interesting part is seeing that greedy "take the biggest coin" fails and a bottom-up DP is required.

**Difficulty: medium** — one DP formulation plus an impossibility case, solvable in ~30 min.

## Input / Output

```
{"amount":<int>,"coins":[<int>,…]}
---
<count>      min coins, or -1 if impossible
```

## Example

```
{"amount":11,"coins":[1,2,5]}
→ 3      5+5+1
```

## Teaches

- **Unbounded-knapsack DP**: `dp[a] = 1 + min over coins c≤a of dp[a-c]`; reusing each coin freely distinguishes this from 0/1 knapsack.
- **Reachability via a sentinel**: seed unreachable amounts with an infinite cost so an untouched `dp[amount]` cleanly maps to `-1`.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS
