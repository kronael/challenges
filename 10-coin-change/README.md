# 10 — Coin Change

**Task**: Make exact change for N cents using the fewest coins, given an unlimited supply of each denomination — or report it's impossible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have an unlimited pile of coins in each given denomination. What's the minimum number of coins that sum to exactly `amount`? Return `-1` if no combination works.

The tempting move is greedy: always grab the largest coin that fits. It works for real-world currency, which is *why* the trap is so easy to fall into — but it's wrong in general (see Example 2). You need a bottom-up DP that builds the best answer for every amount from 0 up to the target.

Constraints: amount up to ~10⁴, denominations are positive ints.

## Input

```json
{"amount": 11, "coins": [1, 2, 5]}
```

## Output

A single integer: minimum coin count, or `-1` if the amount can't be made.

## Examples

**Example 1** — 5 + 5 + 1
```
{"amount":11,"coins":[1,2,5]} → 3
```

**Example 2** — greedy takes 4 then is stuck (4+?), DP finds 3+3 = 2 coins
```
{"amount":6,"coins":[1,3,4]} → 2
```

## Teaches

- **Unbounded-knapsack DP**: `dp[a] = 1 + min over coins c ≤ a of dp[a−c]`; reusing each coin freely is what separates this from 0/1 knapsack.
- **Impossibility via sentinel**: seed unreachable amounts with an infinite cost, so an untouched `dp[amount]` maps cleanly to `-1`.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS
