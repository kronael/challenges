# 07 — Medium — Coin Change

**Task**: Make exact change for N cents using the fewest coins, given an unlimited supply of each denomination — or report it's impossible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have an unlimited pile of coins in each given denomination. What's the minimum number of coins that sum to exactly `amount`? Return `-1` if no combination works.

Constraints: `0 <= amount <= 2,000,000`; denominations are distinct positive integers, at most `100` of them; the list of denominations may be empty.

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

**Example 2**
```
{"amount":6,"coins":[1,3,4]} → 2
```

## Run

```
make -C rust
make -C go
make -C c
make -C python
```

Stuck? See `hints/01.md`.

Source: LeetCode 322, Coin Change
