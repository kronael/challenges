# 23 — 0/1 Knapsack

**Task**: Pack a bag of capacity W to maximise total value, taking each item at most once.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

You're packing a bag with capacity W. Each item has a weight and a value, and you can take each item at most once. Maximise total value without exceeding capacity. The trap: greedy by value/weight ratio fails — a high-ratio item can crowd out a pair that together fills the bag better. You must consider take-or-leave for every item.

## Input

```json
{"capacity": 10, "items": [{"weight":5,"value":10},{"weight":4,"value":40},{"weight":6,"value":30},{"weight":3,"value":50}]}
```

## Output

A single integer: the maximum achievable total value.

## Examples

**Example 1** — best fit combines two mid items, not the single densest
```
capacity 10, items above → 90   (weight 4+3, value 40+50)
```

**Example 2** — greedy ratio trap: the densest item blocks a better pair
```
capacity 10, items [{w:6,v:10},{w:5,v:6},{w:5,v:6}] → 12   (greedy ratio gets only 10)
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
