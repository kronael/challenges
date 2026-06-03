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

- 18-prime-sieve: off-by-one when n is an odd prime. `python/main.py` `solve()`
  counts `n` itself when `n` is an odd prime, but the README says "primes p with
  p < n" (strictly below). Odd-only sieve uses `size = (n+1)//2`, which includes
  value `n` at the top index, and the loop guard `(2*i+1)**2 < n` never strikes
  it. So `solve(3)=2` (should be 1), `solve(5)=3` (should be 2). General n is
  fine; only n = an odd prime is wrong. Test `cases/03` (n=3 -> 2) matches the
  buggy reference, so the suite passes — the stored `.out` is consistent with the
  reference, not with the spec.

- 25-mst: no disconnected-graph detection. `python/main.py` `solve()` returns the
  minimum spanning *forest* weight for a disconnected input instead of signalling
  "no spanning tree". README states the graph is connected, so it is in-spec, but
  a disconnected test case cannot be added meaningfully (e.g. n=4 edges
  [[0,1,5],[2,3,7]] -> 12, not an error). The "disconnected" edge-case category
  is left uncovered for that reason.
