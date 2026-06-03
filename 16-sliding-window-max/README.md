# 16 — Sliding Window Maximum

**Task**: Report the maximum sensor reading in every consecutive window of k readings.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Given a stream of sensor readings and a window size k, find the maximum reading in each consecutive window, left to right. A naive approach rescans k values per window — O(nk) total, which dies on long streams. You need O(n), touching each reading a constant number of times.

## Input

```json
{"k": 3, "arr": [1, 3, -1, -3, 5, 3, 6, 7]}
```

## Output

The maximum of each window, in order, space-separated.

## Examples

**Example 1** — the same max can win several consecutive windows
```
k=3, arr [1,3,-1,-3,5,3,6,7] → 3 3 5 5 6 7
```

**Example 2** — when the max scrolls out, the next-best must already be remembered
```
k=2, arr [9,1,1,1] → 9 1 1
```

## Teaches

- **Monotone deque**: keep window indices in decreasing value order so the front is always the current max; smaller-and-older elements can never win, so drop them.
- **Amortized O(n)**: each index is pushed and popped at most once — no window is ever re-scanned.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: https://leetcode.com/problems/sliding-window-maximum/
