# 10 — Coin Change

**Task**: Make exact change for N cents using the fewest coins, given an unlimited supply of each denomination — or report it's impossible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have an unlimited pile of coins in each given denomination. What's the minimum number of coins that sum to exactly `amount`? Return `-1` if no combination works.

Some familiar coin systems make this look simpler than it is. In general, choosing the largest useful coin first can produce too many coins, and trying every possible assembly can grow far beyond the input size.

Constraints: `0 <= amount <= 2,000,000`; denominations are positive integers. The list of denominations may be empty.

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

**Example 2** — taking 4 first gives 4+1+1, but 3+3 uses fewer coins
```
{"amount":6,"coins":[1,3,4]} → 2
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: CLRS; LeetCode 322 (Coin Change)
