# 40 — Weighted Job Scheduling

**Task**: Given N jobs each with a start time, end time, and profit, select a non-overlapping subset that maximises total profit.

**Difficulty**: medium
**Time estimate**: ~50 min

## Problem

Unlike plain interval scheduling (challenge 11), which maximises the *count* of
jobs, here each job carries a weight and you maximise the *sum*. Earliest-finish
greedy fails: a single fat job can be worth more than the many small jobs it
blocks, or vice versa.

Sort by end time, then DP: for each job, either skip it or take it plus the best
solution ending before it starts. Finding "the latest job that finishes before
this one starts" by binary search makes the whole thing O(n log n).

## Input / Output

```json
{"jobs": [{"start": 0, "end": 6, "weight": 60}, {"start": 1, "end": 4, "weight": 30}, {"start": 3, "end": 5, "weight": 10}, {"start": 5, "end": 9, "weight": 40}]}
```
Single integer: the maximum total weight of a non-overlapping subset.

## Examples

**Example 1** — taking the two outer jobs beats any greedy pick.
```
jobs (0,6,60),(1,4,30),(3,5,10),(5,9,40) → 70
```
Take (0,6,60) + (5,9,40); they don't overlap.

**Example 2** — catches earliest-finish greedy, which would take the small job first.
```
jobs (0,10,5),(1,9,3),(2,8,7),(3,7,4) → 7
```
All overlap, so only one job fits; the heaviest is weight 7.

## Teaches

- **DP on sorted intervals**: sort by end time; `dp[i] = max(skip i, weight[i] + dp[latest compatible])`.
- **Binary search for the predecessor**: `bisect_right(ends, start[i])` finds the latest non-overlapping job in O(log n) — this is what beats the O(n²) inner scan.
- **Why greedy fails**: earliest-finish greedy maximises count, not weight.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [CLRS §16.3](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) · [LeetCode 1235](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)
