# 08 — Longest Increasing Subsequence

**Task**: Find the longest run of strictly increasing stock prices you can pick from a series — the picked days need not be consecutive.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have a stock's closing price for each of `n` successive days. Find the length of the longest streak of strictly increasing prices, where you may choose *any* subset of days (gaps allowed) as long as the chosen prices keep rising.

The obvious DP — for each day, scan all earlier days — is O(n²) and times out around n = 200k. The trick is to maintain an auxiliary array of "best tails" and binary-search it: sorting that array stays automatic, and its length is the answer. Why does that work?

Constraints: n up to 2·10⁵, prices fit in i32.

## Input

```json
{"n": 8, "seq": [3, 1, 4, 1, 5, 9, 2, 6]}
```

## Output

A single integer: the length of the longest strictly increasing subsequence.

## Examples

**Example 1** — the answer skips over the dips; 1,4,5,6 and 1,4,5,9 both reach length 4
```
{"n":8,"seq":[3,1,4,1,5,9,2,6]} → 4
```

**Example 2** — strictly increasing matters: equal values don't extend a run
```
{"n":5,"seq":[2,2,2,2,2]} → 1
```

## Teaches

- **Patience sorting**: `tails[i]` = smallest possible tail of any increasing subsequence of length `i+1`; the array's length is the answer.
- **Binary search to place each element**: `bisect_left` finds where a price extends or improves a pile, turning O(n²) into O(n log n).

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §15.4
