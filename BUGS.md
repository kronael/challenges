# Defect log

## Status — 2026-08-11 — Challenge 35 benchmark review

- **CH35-LARGE-PREFIX-ESCAPE** (HIGH, bench) — Both large fixtures use only
  full-array sums at `35-hard-dynamic-range-sums/cases/09_large_mixed.in:1` and
  `35-hard-dynamic-range-sums/cases/10_large_queries.in:1`; the second has no
  updates, and a correct native prefix array with linear suffix repair passes
  both under the five-second limit. **Fix:** Give both fixtures varied wide
  ranges and enough interleaved low-index updates to make native rescan and
  linear-update controls independently time out with margin.
- **CH35-ROTTEN-DOC-OVERCLAIM** (LOW, docs) — `HINTS.md:23` says the rotten
  reference demonstrates both documented linear strategies, but
  `rotten/main.py:5` implements only range rescanning. **Fix:** State that the
  executable rotten reference demonstrates rescanning and native controls
  validate both strategies.
