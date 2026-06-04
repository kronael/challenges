# 43 — Max Drawdown

**Task**: Given a series of daily prices, find the maximum drawdown — the largest drop from an earlier peak to a later trough.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You are given the price for each of `n` successive days. The *drawdown* of a
later day `j` against an earlier day `i < j` is `price[i] - price[j]`: how far the
price has fallen from that earlier level. The **maximum drawdown** is the largest
such drop over every pair of days with `i < j`:

```
max over i < j of (price[i] - price[j])
```

The trough must come *after* the peak (`i < j`), so you cannot pair a low early
day with a high later day. If prices never fall — every day is at least as high
as all days before it — the maximum drawdown is `0`.

The series is long — up to `n = 2·10⁵` days — and the answer must come back fast.
Comparing every earlier day against every later day is quadratic and will not
finish in time at that scale; part of the challenge is finding a formulation that
does, and not being fooled into pairing the global maximum with the global
minimum when the minimum happens *before* the maximum.

Constraints: `n` up to 2·10⁵, prices fit in i32.

## Input

```json
{"n": 7, "prices": [10, 7, 12, 9, 4, 6, 3]}
```

## Output

A single integer: the maximum drawdown (a non-negative value).

## Examples

**Example 1** — the deepest fall is from the peak 12 (day 2) down to the trough 3 (day 6): 12 − 3 = 9
```
{"n":7,"prices":[10,7,12,9,4,6,3]} → 9
```

**Example 2** — prices only ever rise, so there is no drawdown
```
{"n":4,"prices":[1,2,3,4]} → 0
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: Drawdown (economics) — https://en.wikipedia.org/wiki/Drawdown_(economics)
