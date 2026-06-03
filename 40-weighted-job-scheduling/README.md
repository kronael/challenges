# 40 — Weighted Job Scheduling

Given n jobs each with a start time, end time, and weight, find the maximum
total weight of a non-overlapping subset. Hard because a greedy approach fails
— a high-weight job may block many smaller ones that sum to more.

**Difficulty: medium** — one key insight: reduce to DP + binary search in O(n log n).

## Input / Output

```json
{"jobs":[{"start":0,"end":6,"weight":60},{"start":1,"end":4,"weight":30},...]}
```
```
<maximum weight>   (single integer)
```

## Example

```
jobs: [(0,6,60),(1,4,30),(3,5,10),(5,9,40)]  →  70
```
Take job 1 (weight 60) + job 4 (weight 40); they don't overlap.

## Teaches

- **DP on sorted intervals**: sort by end time; `dp[i] = max(skip job i, take job i + dp[latest compatible])`.
- **Binary search on the answer space**: `bisect_right(ends, start[i])` finds the latest non-overlapping predecessor in O(log n), making the whole algorithm O(n log n).
- **Why greedy fails**: earliest-finish-time greedy maximises *count*, not *weight*; a single high-weight job may dominate many low-weight ones.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [CLRS §16.3](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) · [LeetCode 1235](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)
