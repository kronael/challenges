# Changelog

All notable changes to this challenge bench are recorded here.

## [v0.1.2] — 2026-08-12

> challenges v0.1.2 — seeded benchmarks, smaller checkout
>
> Large benchmarks now regenerate from frozen seeds, cutting 322 MiB from the checkout without weakening correctness or timeout checks.
>
> • `make bench` generates one case at a time and checks it against the golden reference.
> • `make cases` freezes 98 input hashes, seeds, and repeat counts.
> • Challenges 18 and 35 enforce native naive walls with aggregate repeat budgets.
> • Timeout cleanup cannot hang on escaped stderr holders; runtime failures stay failures.
> • Tracked challenge data drops to 9.6 MiB.
>
> Full notes below.

### Changed

- Replaced 196 checked-in large input/output fixtures with 98 deterministic
  recipes whose hashes, seeds, and repeat counts are frozen by `make cases`.
- Generate one benchmark at a time, obtain its expected output from the golden
  reference, compare byte-for-byte, then delete all temporary files.
- Added the existing `check` target to every I/O solver's `make help` output.

### Fixed

- Enforced the challenge 18 and 35 native performance walls with aggregate
  repeat budgets while keeping optimized references well below the limit.
- Bounded every timeout cleanup wait, preserved early runtime failures, rejected
  missing or multiline output, and covered partial temporary-file allocation.

## [v0.1.1] — 2026-08-11

Native benchmark-integrity release. All 48 I/O challenges were audited against
optimized C versions of their intended naive approach, using the five-second
solver budget rather than relying only on Python timing.

### Fixed

- Strengthened both large fixtures wherever an optimized native naive control
  could escape the intended complexity wall: challenges 09, 10, 13, 16, 18, 19,
  23, 24, 26, 28, 35, 39, 41, 42, 46, 51, 53, 54, 55, 56, and 57.
- Regenerated every affected golden output and aligned the documented input
  limits with the enlarged cases.
- Terminated challenge 55's empty expected output with the required newline.

### Changed

- Challenge 23 now documents prefix-answer precomputation with a hash map as a
  valid alternative to its trie-based hint.
- Challenge creation now requires an optimized temporary native control to
  validate each performance wall at the fastest supported solver timeout.
- Added a resolved defect log with the complete native-control audit result.

## [v0.1.0] — 2026-08-10

> challenges v0.1.0 — first tagged snapshot
>
> Cleared a 12-item correctness audit — references now match their specs and
> test suites fail loudly on the states they should catch.
>
> • 41's ordered-set reference answers range counts in O(log n) — no timeout at the op cap
> • 48 and 45 references now handle duplicate/contained reads and repeated k-mers
> • Harnesses reject empty case sets, trailing-whitespace output, and lost-but-duplicated items
> • sys-rotten accepts only a genuine detected defect — crashes and build failures now fail
>
> Full notes below.

First tagged release: the 57-challenge practice bench after clearing the
2026-07-26 codex audit queue (12 findings, C1–CC).

### Fixed

- **41** ordered-set: golden `range_count` was O(n) per query (O(n²) overall) and
  timed out at the documented 10⁵-op cap; rewrote as a rank-augmented skip list,
  O(log n) per query.
- **48** shortest-superstring: golden and rotten skipped the required
  duplicate/contained-read reduction — a wrong answer and a `StopIteration` crash
  on valid input; both now reduce first.
- **45** k-mer assembly: rotten used a Hamiltonian read-chain that was wrong
  whenever a `(k-1)`-mer repeated; rewrote as a correct Hierholzer traversal.
- **07** coin-change: golden could hang on a large coin list; golden now dedups
  and the spec bounds denominations to ≤100 distinct.
- **31** work-stealing deque: the buffer was half its documented capacity
  (`1<<21`); now `1<<22`.
- **30** tick snapshot: the stress miscounted the initial all-zero snapshot as a
  torn read; the tear check now signals torn-ness separately from the value.
- **shared C harness**: `make test` trimmed trailing whitespace while `make bench`
  compared byte-exact; `test` now matches `bench`.
- **sys-rotten** contract: any nonzero exit counted as a controlled failure, so a
  crash or build error passed; now requires the harness's exit-1 detection signal.

### Changed

- **43** and **48** large fixtures trimmed back inside the documented input caps
  (200k orders, 20000 reads).
- **53–57** Go/Rust/Python case harnesses now fail on an empty case set and on
  unread/unparseable expected files (previously a silent pass).
- **21/22/29/33** tests strengthened: coloring distinctness, `sieve` must consume
  its argument, and exact-once identity in the MPSC and stack stresses.
- **30** seqlock: documented the non-atomic-payload C11 data race as the
  intentional textbook tradeoff.
- **21/22** READMEs note the Go track alongside Python.
