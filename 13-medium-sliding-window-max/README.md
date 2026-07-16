# 13 — Medium — Sliding Window Maximum

**Task**: Report the maximum sensor reading in every consecutive window of k readings.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Given a stream of sensor readings and a window size `k`, a window of `k`
consecutive readings slides from the far left of the stream to the far right,
moving one position at a time. For each position, report the maximum reading
visible in the window. The first window covers readings `0..k-1`; the last
covers the final `k` readings. There are `n - k + 1` windows in all.

The stream may be long, and the number of windows can be large. Your program
must produce every requested maximum within the stated limits.

Constraints: `n` up to 2·10⁵, `1 ≤ k ≤ n`, readings fit in i32.

## Input

```json
{"k": 3, "arr": [1, 3, -1, -3, 5, 3, 6, 7]}
```

## Output

The maximum of each window, in order, space-separated.

## Examples

**Example 1**
```
k=3, arr [1,3,-1,-3,5,3,6,7] → 3 3 5 5 6 7
```

**Example 2**
```
k=2, arr [9,1,1,1] → 9 1 1
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

Source: https://leetcode.com/problems/sliding-window-maximum/
