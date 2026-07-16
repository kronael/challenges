# Hints — 47 Hard — RNA Max Pairs

> Spoilers. Open only when stuck.

- **Interval DP.** Let `dp[i][j]` be the maximum number of non-crossing pairs
  achievable inside the substring `rna[i..j]` (inclusive). The answer is
  `dp[0][n-1]`. Build it up over intervals of increasing length, so every
  subinterval you reference is already solved.
- **Two choices for the rightmost base `j`.** Either:
  - `j` is left unpaired → `dp[i][j-1]`, or
  - `j` pairs with some earlier base `k` in `[i, j)` where `rna[k]`/`rna[j]` is an
    allowed pair and `j - k > min_loop`. That pair splits the interval into two
    independent (non-crossing) halves: `dp[i][k-1] + 1 + dp[k+1][j-1]`.
  Take the max over the unpaired option and every valid partner `k`.
- This is the **Nussinov** recurrence. Three nested loops (interval length, left
  endpoint, split point) give **O(n³)** time and **O(n²)** space — fine for
  `n = 400`.
- **Allowed-pair check.** Build the set `{AU, UA, CG, GC}`, and add `{GU, UG}`
  when `allow_wobble` is set. The `min_loop` guard (`j - k > min_loop`) is what
  forbids hairpins that are too tight.

The naive version (`rotten/`) recurses over the same two choices but **without
memoization**, re-solving overlapping subintervals exponentially many times —
correct on tiny strands, TIMEOUTs on the large cases.

Source: Nussinov et al., "Algorithms for loop matchings" (1978),
https://doi.org/10.1137/0135006
