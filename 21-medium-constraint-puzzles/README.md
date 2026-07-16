# 21 — Medium — Constraint Puzzles

**Task**: Implement four functions that return every valid solution to four classic puzzles.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

`main.py` exposes four functions to fill in. Each one returns *all* solutions to a
puzzle:

- `solve_nqueens(n)` — place `n` queens on an `n×n` board so no two attack each
  other (no shared row, column, or diagonal). Return every placement as a tuple
  where index = row and value = column. Valid inputs have `0 <= n <= 8`.
  `n=0` returns `[()]`, `n=4` has 2 solutions, and `n=8` has 92.
- `solve_graph_coloring(n, edges, k)` — assign one of `k` colors to each of the
  `n` nodes so that the two endpoints of every edge get different colors. Return
  every valid coloring as a dict mapping node → color. A triangle has 6 proper
  3-colorings; the complete graph on 4 nodes has none with 3 colors.
- `solve_send_more_money()` — assign a distinct digit `0–9` to each of the
  letters `S E N D M O R Y` so that the addition `SEND + MORE = MONEY` holds, with
  no leading zero on `S` or `M`. Return every assignment as a dict letter → digit.
  There is exactly one.
- `enumerate_splits(lst)` — return every way to cut `lst` into a `(prefix,
  suffix)` pair that concatenates back to `lst`. For `[1, 2, 3]` that is the four
  pairs `([], [1,2,3])`, `([1], [2,3])`, `([1,2], [3])`, `([1,2,3], [])`; for `[]`
  it is the single pair `([], [])`.

The test suite checks exact solution counts and validity.

## Run

```
make -C python
```

Stuck? See `HINTS.md`.
