# Hints — 46 CRISPR Off-Targets

> Spoilers. Open only when stuck.

- **Pigeonhole / seed-and-extend**: split each length-`L` string into `d+1`
  contiguous blocks ("seeds"). If two length-`L` strings are within Hamming
  distance `d`, then by the pigeonhole principle at least one of the `d+1` seeds
  must match *exactly* (you can't spread `d` mismatches across `d+1` blocks
  without leaving one block untouched). So an exact seed match is a *necessary*
  condition for being an off-target — use it as a filter.
- **Index the genome's window seeds**: slice the genome into the same `d+1`
  block positions. For each window start `s` and each block slot `k`, record the
  block substring → list of window starts in a hash map (one map per slot, so a
  seed only matches a seed in the same position). Building this is
  `O(genome × (d+1))`.
- **Look up, then verify**: for each guide, take its `d+1` seeds and gather the
  candidate window starts from the matching slot's map. Deduplicate (a window
  can share several seeds). For each unique candidate, compute the full Hamming
  distance against the guide with an **early exit** — stop the moment the
  mismatch count exceeds `d`. Count the survivors.
- **Why this beats the naive scan**: the index restricts each guide to windows
  that share a seed, instead of all `genome−L+1` windows. The full-length
  comparison runs only on those few candidates.

The naive trap (`rotten/`) is the triple loop: every guide × every window ×
every base. Correct, but `O(guides × genome × L)` — it TIMEOUTs on the large
genome × many-guides case.

Source: Bae, Park & Kim, "Cas-OFFinder", Bioinformatics 30(10):1473 (2014),
https://academic.oup.com/bioinformatics/article/30/10/1473/267560
