# 16 — Sliding Window Maximum

Output the maximum of every length-`k` window of an array, left to right. The challenge is doing it in O(n), not the obvious O(n·k).

## Input / Output

```
{"k":<int>,"arr":[<int>,…]}
---
m0 m1 …      maximum of each window, in order
```

## Example

```
{"k":3,"arr":[1,3,-1,-3,5,3,6,7]}
→ 3 3 5 5 6 7
```

## Teaches

- **Monotone deque**: keep window indices in decreasing value order so the front is always the current max; smaller-and-older elements can never win again, so drop them.
- **Amortized O(n)**: each index is pushed and popped at most once, so the running maximum is maintained without ever re-scanning a window.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: https://leetcode.com/problems/sliding-window-maximum/
