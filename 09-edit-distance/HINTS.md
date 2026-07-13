# Hints — 09 Edit Distance

> Spoilers. Open only when stuck.

- **Compute the Levenshtein distance** — the minimum number of single-character
  insertions, deletions, and substitutions to turn `s` into `t`.
- **2-D dynamic programming**: `dp[i][j]` = distance between prefixes `s[:i]`
  and `t[:j]`. Each cell is the cheapest of insert (`dp[i][j-1] + 1`), delete
  (`dp[i-1][j] + 1`), or substitute (`dp[i-1][j-1] + 0` if the chars match else
  `+ 1`). The first row and column are `0..len`, since matching against an empty
  prefix costs one edit per remaining character. The answer is the bottom-right
  cell. This is O(|s|·|t|) — fast enough for a few thousand characters.
- **Rolling-array space**: filling a cell only ever reads the previous row and
  the current row's left neighbour, so you never need the whole matrix. Keep two
  rows (or one row plus a saved diagonal) and space drops from O(|s|·|t|) to
  O(min(|s|,|t|)).

The naive recursion (`rec(i,j)` branching into insert/delete/substitute with no
memoization) is what `rotten/main.py` does — correct, but exponential, so it
TIMEOUTs on the large cases.

Source: CLRS §15.5
