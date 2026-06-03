# bugs

Review queue. Log here, do not fix unless explicitly asked.

## Open

- **18-prime-sieve**: off-by-one when n is an odd prime. `solve(3)=2` (should be 1),
  `solve(5)=3` (should be 2) — the odd-only sieve counts `n` itself when `n` is an
  odd prime, contradicting the README's "primes p < n" (strictly below). Stored
  `cases/03.out` matches the buggy reference, so the suite passes but the value is
  wrong vs spec. All other n are correct.

- **25-mst**: no disconnected-graph detection. `solve()` returns the spanning-forest
  weight instead of signalling "no spanning tree". README guarantees connectivity so
  it is in-spec, but the "disconnected" edge-case category is deliberately uncovered.

## Resolved

- ~~`37-fenwick-tree`: 12 `.out` files missing trailing newline~~ — fixed.
- ~~`*/go/solution_test.go` (24 files): `\!` + missing `strings` import~~ — fixed.
