# 59 — Medium — Price Undercut

**Task**: For every day of a settlement series, report how many days pass before
that day's price is first undercut.

**Difficulty**: medium
**Time estimate**: ~25 min

## Problem

`prices[i]` is the settlement price of a contract on day `i`, in ticks, and the
series is listed in day order. Day `i` is *undercut* on the first later day that
settles **strictly lower** than `prices[i]`. A later day that settles at exactly
`prices[i]` does not undercut it.

For every day `i` report the wait until it is undercut: `j - i`, where `j` is the
smallest index greater than `i` with `prices[j] < prices[i]`. Report `0` for a
day that is never undercut, including the last day of the series.

Every day of the series gets its own answer, and the series can be long, so the
whole report must be produced within the stated limits.

Constraints: `1 <= n <= 250000`, `n` equals the length of `prices`, and every
settlement price fits in a signed 32-bit integer and may be negative.

## Input

```json
{"n": 6, "prices": [30, 40, 40, 35, 20, 25]}
```

- `n` — number of days in the series
- `prices` — the settlement price of each day, in day order

## Output

The wait for each day, in day order, space-separated on one line. Exactly `n`
integers.

## Examples

**Example 1** — day 0 waits four days for the 20; both 40s are undercut by the 35
```
{"n":6,"prices":[30,40,40,35,20,25]} → 4 2 1 1 0 0
```

**Example 2** — an equal settlement is not an undercut
```
{"n":4,"prices":[50,50,50,50]} → 0 0 0 0
```

**Example 3** — every day but the last is undercut by the very next day
```
{"n":3,"prices":[5,4,3]} → 1 1 0
```

## Run

```
make -C rust
make -C go
make -C c
make -C python
```

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.

Stuck? See `hints/01.md`.

Source: [LeetCode 739 — Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)
