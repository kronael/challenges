# Changelog

All notable changes to this challenge bench are recorded here.

## [Unreleased]

### Added

- **vec challenge type** and challenges 66–68 (Variant Allele Counts, Tick
  Frame Audit, Sparse Activation Gate), graded on the emitted machine code as
  well as the answer. Each has C `golden/` and `rotten/` controls, `cases/`,
  `hints/`, a `vec.mk` naming the traced fixture, and `c/`, `rust/`, and `go/`
  solver scaffolds. `shared/vec.mk` adds `make vec`; the root `make vec`
  checks every golden and rotten under `cc`, and under `clang` too when it is
  on PATH.
- Go solver track for 66–68: `go/` builds with `GOEXPERIMENT=simd` and
  `GOAMD64=v3`, so a solve may use `simd/archsimd`.

### Changed

- Merged v0.1.5 into the vec work. v0.1.4's 58–65 had taken the numbers the
  vec challenges were built under, so they moved from 58–60 to 66–68, and
  their slugs were renamed to solution-neutral titles.
- Every Go module and the template now declare `go 1.27.1`.
- `scripts/vec_check.py` rebuilt as a ptrace tracer. It runs the binary
  `make test` checks on one fixture, single-steps `solve` and everything it
  calls, and passes a solve that retires fewer than one scalar instruction per
  input element. The loop-shape reader it replaces passed any solve with one
  packed loop anywhere and missed SIMD done in helpers. Solver sources may not
  use assembly, pragmas, target or optimize attributes, `#[target_feature]`,
  `build.rs`, or cgo, and AVX-512 is refused at run time. Rust builds and tests
  one release `x86-64-v3` build.
- 66 now sums floating-point dosages; 67 holds frames to 32–1024 bytes wide;
  68 is traced on a full-size 16389-score batch. Their hints moved to `hints/`.
- README and CLAUDE.md count 67 challenges and no longer list the quiz type
  retired in v0.1.4.

### Fixed

- `make vec` found no return from a Go `solve` whose frame made the runtime
  move its stack, and failed a vectorized solve as exiting inside the graded
  function.
- `make vec` gives up after 60 seconds. It used to single-step a `solve` that
  never returned for 400 instructions per input element before failing, and
  wait forever on a program that hung outside `solve`. The traced program no
  longer outlives the grader.
- `make vec` says when the system does not permit ptrace, instead of saying
  that the program could not start.
- Go grades are deterministic: `make vec` no longer counts the runtime growing
  a goroutine's stack, preempting it, or growing the heap, since
  `runtime.morestack` and `runtime.systemstack` run untraced. A Go solve that
  makes a call per vector graded 6.7 to 8.7 scalar instructions per element
  across identical runs and now grades 0.13 every time; one that allocates its
  output graded 0.15 to 0.48 and now grades 0.02.
- `make vec` counts a scalar int-to-float convert from memory and a scalar
  compare with an `_oq`-style predicate as scalar, not packed.
- `make vec` passes the traced program's stderr through and names its exit
  status when it stops early.
- NOTICE points to each challenge's `hints/` instead of `HINTS.md`, and no
  longer lists the retired challenge 40.
- README: the Go stub is `solution.go`, not `main.go`.

## [v0.1.5] — 2026-08-24

> challenges v0.1.5 — defect-queue cleanup
>
> Resolves the `BUGS.md` review queue: real correctness fixes to the Go and C
> solver scaffolds, int64-boundary test coverage, sys Makefile standardization,
> value-checking tests for challenge 22, and solution-neutrality / accuracy
> touch-ups across several READMEs and hints.
>
> • Go/C scaffolds: 64-bit fields no longer narrow to `int` (would overflow on
>   32-bit GOARCH) across challenges 03, 04, 07, 10, 17, 35, 42, 43, 47, 54, 57
> • Adds int64-boundary small fixtures to 01, 02, 28, 49, 52
> • sys (29–34) Makefiles standardized; challenge 22 golden gains value tests
> • Solution-neutral README/hint fixes and ≤/superscript glyph consistency
>
> Full notes below.

### Fixed

- **Go solver scaffolds widened to `int64`** where a documented 64-bit field or
  result was parsed or returned as `int` (overflows on 32-bit `GOARCH`): 03
  (drawdown result), 04 (loads), 07 (coin denominations), 10 (edge weights), 17
  (item value/total), 35 (assignment payload), 42 (query endpoints), 43
  (aggregate quantities/result), 47 (min-loop), 54 (masses), 57 (event IDs).
  Each fix widens `main.go`, `solution.go`, and the expected-output parsing in
  `solution_test.go` together; stubs still build and their harness parses.
- **57 C scaffold**: `Event.id` widened from `int` to `long long`, matching the
  Rust and C answer tracks and the 64-bit output.

### Added

- int64-boundary small fixtures: 01 (an element and sum beyond signed 32-bit),
  02 (a result beyond signed 32-bit), 28 (i64 `ts`/`id`), 49 (a path total
  beyond signed 32-bit), 52 (a minimum assignment total beyond signed 32-bit).
- Challenge 22 golden: value-checking tests for all eight sequence functions
  (previously scaffold/signature-only).

### Changed

- sys challenges 29–34: Makefiles standardized — `CC ?= cc` everywhere (no
  `gcc`/hardcoded `cc`), bare-integer `TIMEOUT`, Rust `bench` builds the release
  binary before the timed run, `help` lists `check`/`help`, and Rust `clean`
  removes the untracked `Cargo.lock`.
- 49/50/51/52 READMEs: added the standard `**Task**`/`**Difficulty**`/`**Time
  estimate**` header and `## Problem` heading used by every other challenge.
- 55 README: reworded the operation-availability line so it no longer telegraphs
  an offline approach. 56 README: removed the "Collinear pairs are not part of
  the count" line (horizontal/vertical segments are never collinear).
- 53/55/56 READMEs: ASCII `<=`/`10^9` replaced with `≤`/`10⁹`.
- 07/10/45 hints: name `rotten/main.py` in the complexity note (10 gains a
  Complexity file) and cite CLRS Problem 16-1 for coin change.
- 59/60/63 hints: benchmark-margin wording made accurate and hardware-robust.
- template/README.md aligned to the canonical challenge layout.
- 37 Rust stub: dropped redundant `Input::size()/limit()` accessors.
- CLAUDE.md: corrected the note about API challenges 21/22 (they have `golden/`).

## [v0.1.4] — 2026-08-24

> challenges v0.1.4 — new challenges + cleaner Go solvers
>
> Eight new trading-themed challenges, Go solvers now read as a plain `solve()`
> function, and every hint set moved to the numbered `hints/` layout.
>
> • Adds challenges 58–65 (kth-worst-fill, price-undercut, venue-ancestor, …)
> • Go: `solve` lives in `solution.go`; `main.go` is only the JSON IO scaffold
> • `HINTS.md` → `hints/01.md…`, one spoiler per file, sources last
> • README novice-clarity pass across every challenge
> • Retires challenge 40 (go-memory-model quiz)
>
> Full notes below.

### Added

- Challenges 58–65 (kth-worst-fill, price-undercut, venue-ancestor,
  critical-venue-links, neutral-basket, liquidity-wall, signal-path,
  strategy-portfolio) — golden/rotten references, five language scaffolds,
  `hints/`, and seeded cases; all pass test/golden/rotten/cases.
- Challenge 24 gains empty-ops, i32-bounds, and zero/negative-key cases.
- `specs/go-solver-layout.md` documenting the Go split.

### Changed

- Go I/O solvers split: `solve` is isolated in `solution.go`; `main.go` holds
  imports, the JSON `input` type, and `main` (decode → solve → print), mirroring
  the Rust lib/main layout. Tests and package-mode build are unchanged.
- Every challenge's `HINTS.md` migrated to numbered `hints/` files.
- README novice-clarity pass across all challenges and the root catalog.
- Challenge 24's rotten reference hardened.

### Removed

- Challenge 40 (go-memory-model quiz).

## [v0.1.3] — 2026-08-14

> challenges v0.1.3 — consistent Rust harnesses
>
> Rust I/O challenges now share one library-first scaffold, typed parsing
> boundaries, and fixture tests that fail loudly.
>
> • All 48 crates expose `solve` from `src/lib.rs`.
> • Binaries only parse input, call `solve`, and print one result.
> • Heterogeneous JSON decoding is isolated in four `src/input.rs` modules.
> • Challenge 24 passes typed operations instead of raw JSON values.
> • Fixture discovery rejects unreadable entries and empty case sets.
>
> Full notes below.

### Changed

- Normalized all 48 Rust I/O crates around `src/lib.rs`, a thin `src/main.rs`,
  and external fixture tests.
- Kept plain input types beside `solve` while isolating heterogeneous JSON
  decoding in `src/input.rs` for challenges 24, 26, 41, and 51.
- Replaced challenge 24's raw JSON solver boundary with typed cache operations.
- Brought the Rust template under the same layout and required a nonempty case
  set before its fixture loop can pass.

### Fixed

- Made Rust fixture enumeration report unreadable directory entries instead of
  silently skipping them.
- Corrected the documented Rust solver path to `src/lib.rs`.

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
