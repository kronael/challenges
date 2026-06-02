# 16 — Sliding Window Maximum

Given an array and a window size `k`, output the maximum of every contiguous window of length `k`, left to right. There are `n - k + 1` windows.

## Input / Output

```
{"k":<int>,"arr":[<int>,…]}
---
m0 m1 …      maximum of each window, in order
```

## Examples

```
{"k":3,"arr":[1,3,-1,-3,5,3,6,7]}
→ 3 3 5 5 6 7

{"k":1,"arr":[4,2,7]}
→ 4 2 7
```

## Key insight

Monotone deque holding indices of a decreasing subsequence: the front is always the window max. Each index is pushed and popped once, giving O(n) versus the naive O(n·k).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
