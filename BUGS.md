# Defect log

## B1 — I/O benchmark controls did not prove the native naive wall (2026-08-10, resolved)

All 48 I/O challenges validate the deliberately naive control only through
`rotten/main.py`, with a 10-second Python timeout. Solver benchmarks instead give
Go, Rust, and C five seconds. Passing the Python timeout contract therefore did
not establish that the documented naive formulation was too slow in a compiled
language. Challenge 23 exposed the gap: a direct native rescan passed both large
fixtures in under one second.

- **Severity:** high
- **Scope:** benchmark validity across all 48 I/O challenges
- **Affected:** I/O large fixtures and the challenge-creation audit procedure
- **Source:** root `Makefile` (`rotten` target) and per-language `bench` targets
- **Audit:** all 48 I/O challenges. Optimized temporary C controls found weak
  fixtures in 09, 10, 13, 16, 18, 19, 23, 24, 26, 28, 35, 39, 41, 42, 46, 51,
  53, 54, 55, 56, and 57. Native controls already timed out for 03, 05, 08, 14,
  27, 50, and 52. The remaining 20 have language-independent work counts far
  beyond the budget.
- **Resolution:** strengthened every weak fixture at documented input limits and
  regenerated its golden output. Every strengthened large case independently
  stops its optimized native control at five seconds. Future challenge audits
  must apply the fastest native timeout as well as the Python rotten timeout.
