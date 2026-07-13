# Hints — 17 Maximum Subarray

> Spoilers. Open only when stuck.

- **DP with a "best ending here" state**: `cur = max(x, cur + x)` decides whether to
  extend the previous run or restart it at `x`; the global best tracks the max over
  all endings. This is the whole trick — do it in one pass and O(1) memory.
- **Online, single-pass**: the recurrence depends only on the prior step, so it
  streams in O(n) time and O(1) space. No prefix-sum array, no nested loop.
- **All-negative case**: because the subarray must be non-empty, the answer is the
  single largest (least negative) element. Seeding `best = cur = arr[0]` and never
  comparing against an empty-subarray sum of 0 handles this for free.

The naive O(n²) approach — sum every `(start, end)` pair and take the max — is what
`rotten/main.py` does. It is correct but TIMEOUTs on the large cases.

Source: CLRS §4.1, maximum-subarray problem
