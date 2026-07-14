# Hints — 48 Hard — Shortest Superstring

> Spoilers. Open only when stuck.

- **The >half-length overlap makes the successor unique.** If two reads `a` and
  `b` both overlapped a read `r` on its suffix by more than half of `r`, those two
  overlaps would themselves overlap inside `r`, forcing `a` and `b` to agree —
  there is at most one read that follows `r`. So the layout is a single chain, and
  the only work is finding each read's one true successor and walking the chain.

- **Index by prefix, don't compare all pairs.** Build a hash map from every prefix
  of every read (only those longer than half the read) to the read it belongs to.
  Then for each read, take its suffixes from longest down to just over half its
  length and look each one up in the map. The first (longest) hit is the unique
  successor. That is O(L) probes per read instead of O(n·L) pairwise comparisons —
  O(n·L) total rather than the O(n²·L) all-pairs table.

- **Find the head and walk once.** The one read that is nobody's successor is the
  start of the chain. From there follow successors, and at each step append only
  the non-overlapping tail of the next read (`next[overlap:]`). Stop after `n`
  reads. The concatenation is the chromosome.

- **Edge cases**: zero reads → empty string; one read → that read.

The naive trap in `rotten/main.py` is repeated greedy merge: every round it
recomputes the best overlap over *all* remaining pairs by sliding-window string
compare, merges the best pair, and repeats — O(n³·L). Correct on the small cases,
TIMEOUT on the many-reads large case.
