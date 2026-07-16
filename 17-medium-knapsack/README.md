# 17 — Medium — 0/1 Knapsack

**Task**: Pack a bag of capacity W to maximise total value, taking each item at most once.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

You're packing a bag with capacity `W`. Each item has a weight and a value, and
you may take each item at most once (no splitting an item, no taking it twice).
Maximise the total value of the packed items without letting their combined
weight exceed `W`.

Constraints: items up to 1000, capacity up to 10⁴, and each weight is a positive
signed 32-bit integer. Values fit in signed 32-bit integers. The result and all
accumulated values must fit in a signed 64-bit integer.

## Input

```json
{"capacity": 10, "items": [{"weight":5,"value":10},{"weight":4,"value":40},{"weight":6,"value":30},{"weight":3,"value":50}]}
```

## Output

A single signed 64-bit integer: the maximum achievable total value.

## Examples

**Example 1** — four items with different weights and values
```
capacity 10, items above → 90   (weight 4+3, value 40+50)
```

**Example 2**
```
{"capacity":10,"items":[{"weight":6,"value":10},{"weight":5,"value":6},{"weight":5,"value":6}]} → 12
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
