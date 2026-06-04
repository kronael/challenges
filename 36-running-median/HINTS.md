# Hints — 36 Running Median

> Spoilers. Open only when stuck.

- **Two-heap invariant**: keep a max-heap for the lower half and a min-heap for
  the upper half, with every value in the lower half ≤ every value in the upper
  half. The median is then a heap top (odd count) or the average of the two tops
  (even count) — O(1) to read.
- **Rebalancing**: after each push, move one element across the boundary so the
  two halves differ in size by at most one. That keeps the median at the tops and
  each insertion at O(log n), turning the naive per-step re-sort into an online
  O(n log n) total.
- **Balanced to within one element**: decide where a new value goes by comparing
  it to the current max-heap top, then fix sizes. The lower half holds the extra
  element on odd counts, so its top is the median there.

The naive approach — re-sort (or insert into a sorted list) the whole prefix at
every step and read its middle — is what `rotten/main.py` does. It is correct but
O(n² log n), so it TIMEOUTs on the large cases.
