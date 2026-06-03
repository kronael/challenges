# bugs

Review queue. Log here, do not fix unless explicitly asked.

- 37-fenwick-tree: `cases/09_large_mixed.out` and `10_large_queries.out` lack a
  trailing newline while the solution's `print` emits one; values are identical
  byte-for-byte. Cosmetic only (test rstrips). All other challenges' `.out`
  files end in a newline; fenwick's small `.out` files also omit it. Inconsistent
  newline convention across the repo.

- `*/go/solution_test.go` (24 files): line 14 has stray backslash
  `if \!strings.Contains(...)` — illegal U+005C character, and `strings` is
  never imported. `go test` fails at setup in every challenge. Pre-existing
  scaffolding corruption, found while auditing test cases.
