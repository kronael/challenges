# Hints — 48 Hard — Shortest Superstring

> Spoilers. Open only when stuck.

- **Use the chain promise.** The README guarantees the unique predecessor and
  successor relationships after duplicate and contained reads are removed. The
  more-than-half condition alone does not prove that uniqueness.

- **Reduce the input first.** Keep one copy of each distinct read, then discard
  any read contained in another. These removals do not change the shortest
  superstring required by the input.

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

Source: [Rosalind — Genome Assembly as Shortest
Superstring](https://rosalind.info/problems/long/)
