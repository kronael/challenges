# Hints — 36 Hard — Matrix Chain Multiplication

> Spoilers. Open only when stuck.

- **Interval DP**: let `dp[i][j]` be the best cost to multiply matrices `i…j`.
  Solve length-2 intervals first, then length 3, …, so every split reuses
  already-solved subproblems.
- **Choosing a split point**: for an interval `i…j`, try each split `k` in
  `[i, j)` and combine `dp[i][k] + dp[k+1][j] + dims[i]·dims[k+1]·dims[j+1]`,
  keeping the minimum. That is O(n³) over the ~n²/2 intervals — fast enough for
  k = 500.
- **Base case**: a single matrix (`i == j`) costs 0; the answer is `dp[0][n-1]`,
  where `n` is the number of matrices.

The naive approach — recursively trying every split point with no memoization —
recomputes the same subranges over and over and runs in exponential (Catalan)
time. That is what `rotten/main.py` does: correct on the small cases, but it
TIMEOUTs on the large ones.

Source: CLRS §15.2, matrix-chain multiplication
