# Hints — 44 Hard — Affine Alignment Score

> Spoilers. Open only when stuck.

- **Three-state DP**: a single score table can't express "am I currently inside a
  gap?", which is exactly what affine penalties depend on. Carry three tables over
  the prefixes `s[:i]`, `t[:j]`:
  - `M[i][j]` — best score of an alignment of `s[:i]` and `t[:j]` whose last
    column is a residue–residue match/mismatch.
  - `X[i][j]` — best score whose last column is a gap in `t` (a residue of `s`
    aligned to a gap; consumes `s`).
  - `Y[i][j]` — best score whose last column is a gap in `s` (consumes `t`).
- **Recurrence** (with `d = gap_open = 11`, `e = gap_extend = 1`):
  - `M[i][j] = max(M, X, Y)[i-1][j-1] + BLOSUM62[s[i-1]][t[j-1]]`
  - `X[i][j] = max(M[i-1][j] - d, X[i-1][j] - e)` — open a fresh gap from a match
    state, or extend an existing gap in `X`.
  - `Y[i][j] = max(M[i][j-1] - d, Y[i][j-1] - e)`
  - The answer is `max(M, X, Y)[n][m]`.
- **Boundaries**: `M[0][0] = 0`. The first row/column is a single leading gap run:
  `X[i][0] = -(d + e·(i-1))`, `Y[0][j] = -(d + e·(j-1))`; the off-states at the
  origin are `-∞`.
- **Complexity**: `O(|s|·|t|)` time, and `O(min(|s|,|t|))` space if you keep only
  the previous row of each table. That is what the golden does.
- The trap (`rotten/main.py`) uses one table and, at each cell, re-scans every
  possible trailing-gap length `k = 1..j` and `k = 1..i`. That is `O(|s|·|t|·
  (|s|+|t|))` — cubic — correct on the small cases but it TIMEOUTs on the large
  ones.
