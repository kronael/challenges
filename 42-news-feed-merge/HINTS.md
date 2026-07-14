# Hints — 42 News Feed Merge

> Spoilers. Open only when stuck.

- **K-way merge with a min-heap**: each feed is already sorted by `(ts, id)`, so you
  never need to sort the whole thing. Seed a binary min-heap with the first
  event of every non-empty feed, then repeatedly pop the smallest and push that
  feed's next event. Popping `N` events with a heap of size `K` costs
  `O(N log K)` — far better than concatenating all events and sorting
  (`O(N log N)`), and it never holds more than `K` events in memory at once.
- **Heap key = full tuple**: push `(ts, feed_index, id, position)`. The `ts` is
  the primary order; ties break first on feed index, then on id, matching the
  expected output. Carrying `position` lets you fetch the next event in that
  feed after a pop.
- **Refill, don't re-seed**: after popping from feed `fi` at index `j`, push
  index `j+1` of the same feed if it exists. The heap only ever shrinks when a
  feed is exhausted, so the loop terminates after exactly `N` pops.
- **Output is interleaved**: emit `ts` then `id` for each popped event, flat on
  one space-separated line.

The naive approach — at every step, scan all `K` feed heads to find the
smallest — is what `rotten/main.py` does. Correct, but `O(N*K)`: it loses the
`O(N log K)` advantage and TIMEOUTs on the large cases with many feeds.

Source: CLRS §6.5
