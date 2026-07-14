# Hints — 13 Medium — Sliding Window Maximum

> Spoilers. Open only when stuck.

- **Monotone deque**: keep window indices in decreasing value order so the
  front is always the current max. A reading that is both smaller and older
  than a later one can never win any future window, so drop it the moment a
  bigger value arrives.
- **One pass, constant work per reading**: scan left to right. Before pushing
  index `i`, pop every index off the back whose value is `≤ arr[i]`. Pop the
  front if it has scrolled out of the window (`front ≤ i - k`). Once `i ≥ k-1`,
  the front of the deque is the answer for the window ending at `i`.
- **Amortized O(n)**: each index is pushed once and popped at most once, so the
  total work is linear — no window is ever re-scanned.

The naive O(nk) approach (recompute `max(arr[i:i+k])` for every window) is what
`rotten/main.py` does — correct, but it TIMEOUTs on the large cases.
