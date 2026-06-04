# Hints — 27 Longest Common Subsequence

> Spoilers. Open only when stuck.

- **2-D prefix DP**: let `dp[i][j]` be the LCS length of the first `i` chars of
  `s` and first `j` of `t`. Fill a grid indexed by prefixes of both strings,
  where each cell builds on the cells above, left, and diagonal. If the two
  current characters match, extend the diagonal (`dp[i-1][j-1] + 1`); otherwise
  take the better of dropping one character from either side
  (`max(dp[i-1][j], dp[i][j-1])`). The answer is the bottom-right cell. This is
  O(|s|·|t|) — it replaces the exponential recursion's repeated work with one
  pass that solves each prefix pair exactly once.
- **Rolling rows**: each row of the grid depends only on the previous one, so
  you can keep just two rows (current and previous) instead of the whole grid,
  giving O(|s|·|t|) time in O(min(|s|,|t|)) space.

The naive exponential recursion (`lcs(i,j)` recursing on `(i-1,j)` and
`(i,j-1)` at every mismatch, with no memoization) is what `rotten/main.py`
does — correct, but it recomputes overlapping subproblems and TIMEOUTs on the
large cases.
