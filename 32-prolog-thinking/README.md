# 32 — Relational Programming

**Task**: Implement four classic puzzles as relations — declare what a solution *looks like* (variables, the values they may take, and the conditions that must hold) and produce *every* solution, instead of writing a search loop by hand.

**Difficulty**: hard
**Time estimate**: ~40 min

## Problem

`main.py` exposes four functions to fill in. Each one returns *all* solutions to a
puzzle:

- `solve_nqueens(n)` — place `n` queens on an `n×n` board so no two attack each
  other (no shared row, column, or diagonal). Return every placement as a tuple
  where index = row and value = column. `n=4` has 2 solutions; `n=8` has 92.
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

The hard part is the mental shift. The instinct is to write the search yourself —
a nested loop that tries a queen, checks for a clash, backtracks, repeats. Resist
it. State the conditions a solution must satisfy and recover the full set of
solutions from that description. A relation says nothing about *how* to find an
answer, only *what makes one valid* — and the same description that recognises a
valid solution can also enumerate them all.

The test suite checks both the answers (exact solution counts and validity) and
that you arrived at them this way rather than by hand-rolling the search.

## Run

```
cd python && make
```

Stuck? See `HINTS.md`.

Source: relational / logic programming (Prolog)
