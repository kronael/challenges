# 17 — Maximum Subarray (Kadane)

Find the largest sum of any contiguous, non-empty subarray.

## Input / Output

```
{"arr":[<int>,…]}
---
<sum>      maximum contiguous subarray sum
```

## Examples

```
{"arr":[-2,1,-3,4,-1,2,1,-5,4]}
→ 6

{"arr":[-5,-2,-8]}
→ -2
```

## Key insight

Kadane: scan once tracking the best subarray ending at the current index (`cur = max(x, cur + x)`) and the global best. O(n) online DP.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
