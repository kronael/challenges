# Hints — 10 Coin Change

> Spoilers. Open only when stuck.

- **Build the answer bottom-up**: don't search combinations top-down. Solve the
  smallest amounts first and reuse those answers. Compute the best count for every
  amount from `0` up to the target, in order — by the time you reach `amount`, each
  sub-result it depends on is already known.
- **Unbounded-knapsack DP**: `dp[a] = 1 + min over coins c ≤ a of dp[a−c]`; reusing
  each coin freely is what separates this from 0/1 knapsack. This runs in
  O(amount × #coins), which clears the large cases easily.
- **Impossibility via sentinel**: seed unreachable amounts with an infinite cost
  (e.g. `amount + 1`), so an untouched `dp[amount]` maps cleanly to `-1`.

The naive reference in `rotten/main.py` is correct but intentionally slow: it checks
every split of every amount instead of iterating over the small denomination list.
That quadratic scan still passes the small cases, then TIMEOUTs on the large ones.
