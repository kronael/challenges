# 11 — Interval Scheduling

Given `n` intervals `[start, end]`, select the maximum number of pairwise non-overlapping intervals. Intervals touching at an endpoint (one ends where the next starts) do not overlap.

## Input / Output

```
{"n":<int>,"intervals":[[start,end],…]}
---
<count>      maximum number of non-overlapping intervals
```

## Examples

```
{"n":4,"intervals":[[1,3],[2,4],[3,5],[4,6]]}
→ 2

{"n":3,"intervals":[[1,2],[2,3],[3,4]]}
→ 3
```

## Key insight

Greedy: sort by end time and always take the interval that finishes earliest among those compatible with the last pick. O(n log n) from the sort.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
