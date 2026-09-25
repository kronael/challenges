# 65 — Hard — Strategy Portfolio

**Task**: Pick which candidate strategies a firm activates, honouring every
prerequisite, so that the total P&L of the activated set is as large as possible.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

A firm is deciding what to run next session. It holds `n` candidate strategies
numbered `0 .. n-1`. Activating strategy `i` adds `pnl[i]` to the session total —
a negative `pnl[i]` is a strategy that costs the firm more than it brings in, such
as a market-data feed or a hedging leg that only earns its keep through something
else.

The candidates are not independent. `requires` is a list of pairs. A pair
`[a, b]` means strategy `a` cannot run unless strategy `b` runs as well: `b` is a
**prerequisite** of `a`. So activating `a` commits the firm to `b`, and to
whatever `b` in turn requires, and so on.

Choose the set of strategies to activate. The set is valid when it honours every
listed pair: for each `[a, b]` in `requires`, if `a` is in the set then `b` is in
the set too. Report the largest total `pnl` that any valid set reaches.

The empty set honours every pair, so the answer is never below zero — a firm that
likes none of its candidates activates none of them and books nothing.

## Constraints

- `1 <= n <= 50000`, and `pnl` has exactly `n` entries
- `requires` holds between `0` and `200000` pairs
- `-1000000000 <= pnl[i] <= 1000000000`; a strategy may contribute exactly nothing
- in every pair `[a, b]`, both `a` and `b` are strategy numbers in `0 .. n-1`
- the same pair may appear more than once, and `a` may equal `b` — a strategy that
  lists itself as its own prerequisite, which any set holding it already honours
- prerequisites may run in circles: `[a, b]` and `[b, a]` may both appear, and a
  longer loop of prerequisites is valid input too. The rule above still reads the
  same way, so every strategy on such a loop needs every other one on it
- a prerequisite need not carry a lower number than the strategy that names it, and
  the pairs arrive in no particular order
- the answer fits in a signed 64-bit integer

## Input

```json
{"n": 5, "pnl": [12, -5, 30, -8, -40], "requires": [[0, 1], [2, 3]]}
```

- `n` — how many candidate strategies there are
- `pnl` — `pnl[i]` is what activating strategy `i` contributes
- `requires` — each entry `[a, b]` says activating `a` requires activating `b`

## Output

A single integer: the largest total `pnl` of a valid activation set.

## Examples

**Example 1** — strategy `0` earns `12` but needs `1`, which costs `5`, and `2`
earns `30` but needs `3`, which costs `8`; both pairs are worth it, and `4` is left
out
```
{"n":5,"pnl":[12,-5,30,-8,-40],"requires":[[0,1],[2,3]]} → 29
```

**Example 2** — the only earner needs both loss-makers, and `100 - 60 - 60` is
worse than activating nothing
```
{"n":3,"pnl":[100,-60,-60],"requires":[[0,1],[0,2]]} → 0
```

**Example 3** — strategies `1` and `2` share the prerequisite `0`, which the firm
pays for once; `3` needs nothing and is taken as well
```
{"n":4,"pnl":[-30,20,25,5],"requires":[[1,0],[2,0]]} → 20
```

**Example 4** — the two strategies are each other's prerequisite, so they are
activated together or not at all, and together they earn `30`
```
{"n":2,"pnl":[50,-20],"requires":[[0,1],[1,0]]} → 30
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
