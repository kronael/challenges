# Hints — 40 Weighted Job Scheduling

> Spoilers. Open only when stuck.

- **Why greedy fails**: earliest-finish greedy maximises the *count* of jobs,
  not their total weight. With weights, the optimal set can leave gaps a greedy
  pass would have filled, so you must compare whole compatible sets by value.
- **DP on sorted intervals**: sort the jobs by end time, then process them in
  that order. For each job define
  `dp[i] = max(skip job i, weight[i] + dp[latest compatible job])`, where the
  "latest compatible job" is the last one whose end time is `≤` this job's start
  time. The answer is the best `dp` value over all jobs.
- **Binary search for the predecessor**: with jobs sorted by end time, the
  compatible-predecessor index is `bisect_right(ends, start[i])` — the latest
  non-overlapping job in O(log n). That replaces the O(n²) inner scan that pairs
  every job with every earlier one, giving an overall O(n log n).
- **Watch the accumulator width**: total profit can exceed 32 bits even though
  each weight fits in 32. Use a 64-bit accumulator.

The naive O(n²) DP (for each job, scan all earlier jobs to find the best
compatible predecessor) is what `rotten/main.py` does — correct, but it
TIMEOUTs on the large case.

Sources: [CLRS §16.3](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) and [LeetCode 1235](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)
