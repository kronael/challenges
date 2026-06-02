# 23 — 0/1 Knapsack

Given a knapsack of integer `capacity` and a list of items each with a `weight` and `value`, choose a subset whose total weight is at most the capacity and whose total value is maximal. Each item is taken whole or not at all.

## Input / Output

```
{"capacity":<int>,"items":[{"weight":<int>,"value":<int>},…]}
---
<int>      maximum achievable total value
```

## Examples

```
{"capacity":10,"items":[{"weight":5,"value":10},{"weight":4,"value":40},{"weight":6,"value":30},{"weight":3,"value":50}]}
→ 90

{"capacity":1,"items":[{"weight":2,"value":100}]}
→ 0
```

## Key insight

Dynamic programming over capacity: `dp[w]` = best value using a fixed-weight budget `w`. Process items one at a time, iterating `w` downward so each item is used at most once. O(n·W).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
