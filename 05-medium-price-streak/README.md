# 05 — Medium — Price Streak

**Task**: Given a stock's daily closing prices, find the length of the longest run of strictly rising prices you can pick — the chosen days need not be consecutive.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You are given the closing price for each of `n` successive trading days. Pick a
subsequence of days (gaps allowed, original order kept) whose prices are
*strictly* increasing, and make that subsequence as long as possible. Output its
length.

"Subsequence", not "substring": you may skip any days you like, but you cannot
reorder them. Strictly increasing means equal prices do not extend a run.

Constraints: `0 <= n <= 2·10⁵`, `n` equals the length of `seq`, and each value
fits in a signed 32-bit integer.

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

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
