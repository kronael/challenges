# 64 — Medium — Signal Path

**Task**: Find the largest total P&L carried by any chain of desks that links two
desks of a trading hierarchy.

**Difficulty**: medium
**Time estimate**: ~35 min

## Problem

A firm's trading hierarchy holds `n` desks numbered `0 .. n-1`. Every desk has at
most two sub-desks: `left[i]` and `right[i]` name them, and a slot holds `-1` when
the desk has no sub-desk there. Desk `root` sits at the top and is nobody's
sub-desk. `pnl[i]` is what desk `i` contributed on its own over the session; a
desk that lost money contributes a negative number.

Pick two desks `a` and `b`, possibly the same desk twice. Exactly one chain of
desks links them in the hierarchy: it starts at `a`, ends at `b`, and every
consecutive pair on it is a desk together with one of that desk's sub-desks. Call
that chain the **signal path** of `a` and `b`. Its total is the sum of the
contributions of every desk on it, both ends included.

Report the largest total that any signal path carries.

Because `a` and `b` may be the same desk, a signal path always holds at least one
desk. So a hierarchy in which every desk lost money still has an answer.

## Constraints

- `1 <= n <= 500000`, and `pnl`, `left`, and `right` each have exactly `n` entries
- `-1000000000 <= pnl[i] <= 1000000000`; a desk may contribute exactly nothing
- `left[i]` and `right[i]` are each either a desk number in `0 .. n-1` or `-1`
- `0 <= root < n`, and `root` is the one desk that appears in neither `left` nor
  `right`
- every other desk appears exactly once across the two arrays, and following
  sub-desks from `root` reaches every desk: the hierarchy is one tree
- a sub-desk's number may be smaller or larger than its own desk's number, and
  `root` is not necessarily desk `0`
- the hierarchy may be a single line of desks, an even split at every level, or
  any shape in between
- every signal path total and the reported answer fit in a signed 64-bit integer

## Input

```json
{"n": 7, "root": 0, "pnl": [-10, 9, 20, 3, 4, 15, 7], "left": [1, 3, 5, -1, -1, -1, -1], "right": [2, 4, 6, -1, -1, -1, -1]}
```

- `n` — number of desks
- `root` — the desk at the top of the hierarchy
- `pnl` — `pnl[i]` is desk `i`'s own contribution
- `left` — `left[i]` is desk `i`'s first sub-desk, or `-1`
- `right` — `right[i]` is desk `i`'s second sub-desk, or `-1`

## Output

A single integer: the largest total that any signal path carries.

## Examples

**Example 1** — the chain `5 – 2 – 6` totals `15 + 20 + 7 = 42`; every chain that
reaches desk `0` pays its `-10`, and the best of those totals `38`
```
{"n":7,"root":0,"pnl":[-10,9,20,3,4,15,7],"left":[1,3,5,-1,-1,-1,-1],"right":[2,4,6,-1,-1,-1,-1]} → 42
```

**Example 2** — one desk, so `a` and `b` have to be that desk
```
{"n":1,"root":0,"pnl":[-7],"left":[-1],"right":[-1]} → -7
```

**Example 3** — every desk lost money, so the best chain is the single desk that
lost the least
```
{"n":3,"root":0,"pnl":[-3,-5,-1],"left":[1,-1,-1],"right":[2,-1,-1]} → -1
```

**Example 4** — the chain `3 – 1 – 0` totals `20 + 10 + 5 = 35`; carrying on to
desk `2` would pay its `-50`
```
{"n":4,"root":0,"pnl":[5,10,-50,20],"left":[1,3,-1,-1],"right":[2,-1,-1,-1]} → 35
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
