# 63 — Hard — Liquidity Wall

**Task**: Find the largest single sweep that lifts the same quantity from every
level of one contiguous run of price levels.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

A book shows the liquidity resting at `n` consecutive price levels, listed in
price order. `quantities[i]` is the quantity resting at level `i`.

A **sweep** is a choice of two things: a contiguous run of levels `l .. r` with
`l <= r`, and one **uniform quantity** `q` to lift from every level of that run.
The sweep is fillable only if each level in the run rests at least `q`, that is
`q <= quantities[i]` for every `i` from `l` to `r`. A fillable sweep lifts
`q * (r - l + 1)` in total.

Report the largest total that any fillable sweep lifts.

A run may be a single level or the whole book, and `q` may be any non-negative
integer that run supports, so a book resting nothing at all still has an answer.

## Constraints

- `1 <= n <= 1000000`, and `n` equals the number of entries in `quantities`
- `0 <= quantities[i] <= 10^9`; a level may rest nothing
- quantities may repeat, and the book follows no particular shape — it may rise,
  fall, or do both
- every fillable sweep's total and the reported answer fit in a signed 64-bit
  integer

## Input

```json
{"n": 7, "quantities": [200, 100, 500, 600, 200, 300, 100]}
```

- `n` — number of price levels in the book
- `quantities` — the quantity resting at each level, in price order

## Output

A single integer: the largest total that any fillable sweep lifts.

## Examples

**Example 1** — 500 from each of levels 2 and 3 lifts 1000; the deepest level on
its own lifts only 600, and 100 from all seven levels lifts only 700
```
{"n":7,"quantities":[200,100,500,600,200,300,100]} → 1000
```

**Example 2** — every level rests the same, so one sweep takes the whole book
```
{"n":5,"quantities":[400,400,400,400,400]} → 2000
```

**Example 3** — level 2 rests nothing, so no fillable sweep with `q` above 0
spans it; the best is 300 from the two levels on one side
```
{"n":5,"quantities":[300,300,0,300,300]} → 600
```

**Example 4** — 600 from the deepest level lifts 600, while 300 from levels 2
through 5 lifts 1200
```
{"n":6,"quantities":[100,200,300,400,500,600]} → 1200
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
