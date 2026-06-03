# 36 — Running Median

**Task**: Read a stream of integers and report the median after each insertion.

**Difficulty**: medium
**Time estimate**: ~45 min

## Problem

After every number arrives, output the current median: the middle value at odd
count, the average of the two middle values at even count. Re-sorting the prefix
each step is O(n log n) per insertion — O(n² log n) over a 200k stream, far too
slow.

Keep two heaps: a max-heap of the lower half and a min-heap of the upper half,
balanced to within one element. Each insertion is O(log n), and the median is
always one or two heap tops away.

## Input / Output

```json
{"stream": [1, 2, 3, 4]}
```
Space-separated medians, one per insertion: an integer at odd count, a
one-decimal float at even count.

## Examples

**Example 1** — alternates integer (odd count) and `.x` float (even count).
```
[1,2,3,4] → 1 1.5 2 2.5
```

**Example 2** — order of arrival is scrambled; the structure must stay balanced.
```
[5,15,1,3,2,8,7,9,10,6,11,4] → 5 10.0 5 4.0 3 4.0 5 6.0 7 6.5 7 6.5
```

## Teaches

- **Two-heap invariant**: max-heap holds the lower half, min-heap the upper half, every lower value ≤ every upper value; the median is a heap top or the average of the two tops.
- **Rebalancing**: after each push, move one element across so the sizes differ by at most one — keeping the median O(1) to read.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [LeetCode 295 — Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)
