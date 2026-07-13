# Hints — 23 0/1 Knapsack

> Spoilers. Open only when stuck.

- **Consider take-or-leave for every item.** The greedy value/weight ratio sort
  fails because a single dense item can block a better-fitting pair, so you have
  to weigh keeping vs. dropping each item against every reachable budget.
- **1-D DP, right-to-left scan**: `dp[w]` is the best value achievable for budget
  `w`. For each item, iterate capacity *downward* (`W → weight`) when adding it;
  scanning downward guarantees each item contributes at most once. The answer is
  `dp[W]`.
- **Pseudo-polynomial cost**: O(n·W) depends on the numeric capacity, not just
  the item count — the classic distinction from truly polynomial DP. With
  capacity up to 10⁴ and 1000 items this is fast; enumerating every subset (2ⁿ)
  is not.

The naive exponential approach (try every subset, or recurse take/skip with no
memo) is what `rotten/main.py` does — correct, but it TIMEOUTs on the large cases.

Source: CLRS §15
