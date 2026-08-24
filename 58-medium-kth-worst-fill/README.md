# 58 — Medium — Kth Worst Fill

**Task**: Report the k-th worst fill of a trading session for each requested rank.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

An execution log holds the slippage of every fill in one finished trading
session. `slippage[i]` is the slippage of fill `i` in ticks: positive means the
fill printed worse than the quoted price, negative means it printed better, zero
means it printed at the quote. One fill is *worse* than another when its
slippage is larger.

Rank the fills from worst to best and number them from 1. Equal slippage values
occupy separate ranks, so if the two worst fills both slipped 7 ticks then rank 1
and rank 2 are both 7. The `k`-th worst fill of the session is the value at rank
`k`.

The whole log is handed to you before any rank is asked for, and it does not
change afterwards. Report the slippage of the k-th worst fill for every `k` in
`ks`, in the order the ranks are listed.

Constraints: `1 <= n <= 400000`, `n` equals the length of `slippage`,
`1 <= len(ks) <= 8`, every rank satisfies `1 <= k <= n`, ranks may repeat, and
every slippage value fits in a signed 32-bit integer.

Follow-up: solve it in O(n) expected time and O(1) extra space beyond one
copy of the log.

## Input

```json
{"n": 5, "slippage": [3, -1, 7, 3, 0], "ks": [1, 3]}
```

- `n` — number of fills in the log
- `slippage` — slippage of each fill in ticks, in log order
- `ks` — the ranks to report; rank 1 is the worst fill

## Output

The slippage of the k-th worst fill for each rank in `ks`, in the order given,
space-separated on one line.

## Examples

**Example 1** — worst to best the log reads 7, 3, 3, 0, -1
```
{"n":5,"slippage":[3,-1,7,3,0],"ks":[1,3]} → 7 3
```

**Example 2** — equal values hold separate ranks
```
{"n":4,"slippage":[4,4,4,4],"ks":[1,4]} → 4 4
```

**Example 3** — rank `n` is the best fill of the session, and a rank may repeat
```
{"n":3,"slippage":[-5,2,-5],"ks":[3,1,3]} → -5 2 -5
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

Source: [LeetCode 215 — Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)
