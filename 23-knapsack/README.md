# 23 — 0/1 Knapsack

Pick a subset of items fitting an integer `capacity` that maximizes total value, each item taken whole or not at all. The challenge is the "0/1" constraint: an item must not be reused.

## Input / Output

```
{"capacity":<int>,"items":[{"weight":<int>,"value":<int>},…]}
---
<int>      maximum achievable total value
```

## Example

```
{"capacity":10,"items":[{"weight":5,"value":10},{"weight":4,"value":40},{"weight":6,"value":30},{"weight":3,"value":50}]}
→ 90      (items of weight 4 + 3 + ... = value 40+50)
```

## Teaches

- **1-D DP, right-to-left scan**: `dp[w]` is the best value for budget `w`; iterating capacity downward when adding an item guarantees each item contributes at most once.
- **Pseudo-polynomial cost**: O(n·W) depends on the numeric capacity, not just the item count — the classic distinction from truly polynomial DP.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: CLRS §15
