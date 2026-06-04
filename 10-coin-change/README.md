# 10 — Coin Change

**Task**: Make exact change for N cents using the fewest coins, given an unlimited supply of each denomination — or report it's impossible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have an unlimited pile of coins in each given denomination. What's the minimum number of coins that sum to exactly `amount`? Return `-1` if no combination works.

The tempting move is greedy: always grab the largest coin that fits. It works for real-world currency, which is *why* the trap is so easy to fall into — but it's wrong in general (see Example 2). The other trap is enumerating combinations: the number of ways to assemble an amount explodes exponentially, so any approach that tries them all blows up long before `amount` gets large.

Constraints: `amount` up to 2·10⁶, denominations are positive ints.

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

**Example 2** — greedy takes 4 then is stuck (no way to make the remaining 2), but 3+3 = 2 coins
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
