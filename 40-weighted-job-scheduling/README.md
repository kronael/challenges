# 40 — Weighted Job Scheduling

**Task**: Given N jobs each with a start time, end time, and profit, select a non-overlapping subset that maximises total profit.

**Difficulty**: medium
**Time estimate**: ~50 min

## Problem

You are given `n` jobs. Job `i` runs over the half-open interval
`[start, end)` and pays `weight` if you run it. Choose a subset of jobs that do
not overlap in time and maximise the total weight collected. A job that ends at
time `X` does not conflict with one that starts at time `X`.

This is *weighted* scheduling, not plain interval scheduling (challenge 11):
there you maximise the *count* of jobs, here each job carries a weight and you
maximise the *sum*. That difference is the trap — one fat job can be worth more
than the many small jobs it blocks, or worth less than them, and you cannot
tell which without weighing whole compatible sets against each other.

The job count is large — up to `n = 10⁵`. Trying every job against every
earlier job to find which ones it can follow is quadratic and will not finish in
time at that scale; part of the challenge is finding a formulation that does.

Constraints: `n` up to 10⁵; start, end and weight fit in 32-bit integers
(`start < end`, `weight ≥ 0`). The total profit can exceed 32 bits.

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

**Example 2** — a single heavy job can beat several light ones.
```
jobs (0,10,5),(1,9,3),(2,8,7),(3,7,4) → 7
```
All overlap, so only one job fits; the heaviest is weight 7.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: [CLRS §16.3](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) · [LeetCode 1235](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)
