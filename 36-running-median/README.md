# 36 — Running Median

Read a stream of integers one at a time. After **each** insertion, report the
median of everything seen so far. With an odd count the median is the single
middle value (print it as an integer); with an even count it is the average of
the two middle values (print it as a float with one decimal place, e.g. `1.5`).

The naive approach re-sorts after every insertion — O(n² log n) overall. The
challenge is to answer each query in O(log n) so a 200k-element stream stays
fast.

## Input / Output

```
{"stream":[<int>,…]}
---
m1 m2 …      median after each insertion, space-separated
```

`mᵢ` is an integer when `i` is odd and a one-decimal float when `i` is even.

## Examples

```
{"stream":[5,15,1,3,2,8,7,9,10,6,11,4]}
→ 5 10.0 5 4.0 3 4.0 5 6.0 7 6.5 7 6.5

{"stream":[1,2,3,4]}
→ 1 1.5 2 2.5
```

## Constraints

- `1 ≤ len(stream) ≤ 10⁵` (large case: 2·10⁵)
- values fit in `i32`

## Key insight

Keep two heaps. A **max-heap** holds the lower half of the values seen so far;
a **min-heap** holds the upper half. Push each new value into the half it
belongs to, then rebalance so the two sizes differ by at most one (the lower
half may hold the extra element). The median is then the top of the larger
heap, or — when the sizes are equal — the average of the two tops. Each
insertion does O(log n) heap work; reading the median is O(1).

## Run

```
cd python && make test && make bench
cd go     && make test && make bench
cd rust   && make test && make bench
```

Source: [LeetCode 295 — Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.
