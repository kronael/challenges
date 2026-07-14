# Hints — 05 Medium — Price Streak

> Spoilers. Open only when stuck.

- **Patience sorting**: keep an auxiliary array `tails`, where `tails[i]` is the
  smallest possible final price of any strictly increasing run of length `i+1`.
  Scan the prices left to right, placing each into `tails`. The length of `tails`
  at the end is the answer.
- **Binary search to place each element**: for each price, binary-search `tails`
  for the leftmost slot `≥` it (`bisect_left`). If it lands past the end, the
  price extends the longest run so far (`append`); otherwise it overwrites that
  slot, lowering a tail without changing any run length. That turns the naive
  O(n²) scan into O(n log n).
- **Strictly increasing vs non-decreasing**: `bisect_left` (leftmost `≥`) gives
  *strictly* increasing; `bisect_right` would give non-decreasing. This problem
  wants strict, so use `bisect_left`.

The naive O(n²) DP (`dp[i] = 1 + max(dp[j] for j<i if seq[j]<seq[i])`) is what
`rotten/main.py` does — correct but it TIMEOUTs on the large cases.

Source: CLRS §15.4, longest increasing subsequence
