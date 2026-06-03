# 17 — Maximum Subarray (Kadane)

Find the largest sum over any contiguous, non-empty subarray. The insight is that the answer needs only one pass and O(1) memory.

## Input / Output

```
{"arr":[<int>,…]}
---
<sum>      maximum contiguous subarray sum
```

## Example

```
{"arr":[-2,1,-3,4,-1,2,1,-5,4]}
→ 6      (subarray [4,-1,2,1])
```

## Teaches

- **DP with a "best ending here" state**: `cur = max(x, cur + x)` decides whether to extend the previous subarray or restart; the global best tracks the max over all endings.
- **Online, single-pass**: the recurrence depends only on the prior step, so it streams in O(n) time and O(1) space.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: CLRS §4.1
