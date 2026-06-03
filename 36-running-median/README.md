# 36 — Running Median

Read integers one at a time and report the median after each insertion (200k stream).
Medium because re-sorting after every insertion is O(n² log n); the two-heap structure answers each query in O(log n).

## Input / Output
```
{"stream":[<int>,…]}
---
m1 m2 …    median after each insertion; integer at odd count, one-decimal float at even count
```

## Teaches

- **Two-heap invariant**: a max-heap holds the lower half, a min-heap the upper half, with every lower value ≤ every upper value; the median is a heap top (or the average of the two tops).
- **Rebalancing**: after each push, move one element across so the sizes differ by at most one — keeping the median O(1) to read.

## Run
```
cd rust   && make
cd go     && make
cd python && make
```
Source: [LeetCode 295 — Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)
