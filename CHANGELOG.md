# Changelog

All notable changes to this challenge bench are recorded here.

## [v0.1.10] — 2026-09-28

> challenges v0.1.10 — no vec level where SIMD is free
>
> 17 drops `make vec`: its textbook solution already grades vectorized with no
> SIMD code, so the level asked for nothing.
>
> • 17 is an ordinary io challenge again: `make test` and `make bench`
> • 13, 44, and 46 keep `make vec`; their plain solutions grade scalar
>
> Full notes below.

### Changed

- 17 loses its vec level: `vec.mk`, `vec.in`, and `vec.out` are gone, its
  golden is the Python reference again, its solver Makefiles are the io ones
  (Rust `make bench` times the debug build), and its README and hints drop
  level 3.
- `VEC-WORK-BEFORE-SOLVE` is ruled by design: `make vec` grades `solve` and
  does not police work done before it.

## [v0.1.9] — 2026-09-27

> challenges v0.1.9 — every bench wall holds against native code
>
> Every large case now times out a plain native copy of the naive solution,
> even at `-O3 -march=native`, and the docs match what the repo runs.
>
> • 15 challenges get bigger or reshaped large cases; 10 READMEs raise a size limit
> • `make golden` and `make rotten` now also cover the systems challenges
> • READMEs fixed where an example, caption, or field name was wrong
> • `make rotten` no longer needs gigabytes of memory for 38
>
> Full notes below.

### Changed

- Large cases of 03, 09, 11, 14, 16, 19, 26, 27, 35, 41, 43, 52, 56, 57, and
  59 grow or change shape, so a native copy of `rotten/` at `-O2` or
  `-O3 -march=native` runs past the 5 s solver timeout on every one, and each
  golden still passes with room to spare.
- README size limits raised: 03 and 09 (n), 11 (n, friendships, queries),
  19 (n), 26 (n, queries), 27 (n), 43 (orders), 56 (segments), 57 (events),
  59 (n).
- `make golden` runs the systems goldens' stress tests and `make rotten` the
  systems rottens' checks; the `sys` and `sys-rotten` targets are gone.
- `CLAUDE.md` says Rust `make bench` times the debug build on purpose (release
  in 13, 17, 44, and 46), and gives C's 5 s timeout.

### Fixed

- 02 names its modulus `mod`, the input field; 04's Example 2 uses feasible
  fixed loads; 22 documents Go's `unfold`; 41's and 44's captions and 49's
  output line say what they show; 59 drops a line that urged speed.
- The template's Run section lists the C track and the first hint.
- `make vec`'s lint reads the preprocessed C, refuses Rust, Cargo, and Go
  paths that reach outside the solver directory, and refuses a
  `.cargo/config.toml` or a solver Makefile that replaces a shared recipe.
- 38's rotten keeps its memory at O(n); it held 2–3 GB when `make rotten`
  stopped it, enough to push a busy box into swap.

### Known

- 41 range and 46 keep walls under 2×, and 16 and 46 have simple variants that
  no input size separates from the golden; `BUGS.md` records each.

## [v0.1.8] — 2026-09-26

> challenges v0.1.8 — a fairer `make vec`, fewer spoilers
>
> Blind solvers and hostile reviewers worked through the new level; `make vec` now
> grades only `solve` and says where a failing one spent its scalar work.
>
> • `make vec` ignores the solver's own flags, and threads started before `solve`
> • A failed grade names the source lines that did the most scalar work
> • Grades no longer depend on machine load or lazy symbol binding
> • READMEs stop describing the solution's shape; first hints are gentler
> • Python stubs reach their tests again, with ruff pinned
>
> Full notes below.

### Fixed

- `make vec` builds with only the flags `shared/vec.mk` sets, so a solver's
  `-ffast-math` or `RUSTFLAGS` no longer turns a scalar loop "vectorized".
- `make vec` pauses every other thread while `solve` runs and refuses a live
  child process, so work handed to a thread or process started earlier no
  longer escapes the trace.
- The trace stops at 16 M instructions instead of a 60 s wall clock, so a
  correct solve no longer fails on a busy machine.
- Library functions bind at startup, so `solve` is not charged for the
  dynamic linker's lookups (46 C: 0.56 → 0.27 scalar).
- An iteration that runs packed work counts as a vector iteration, whether or
  not the compiler hoisted its loads; zeroing a register marks nothing.
- Only `%rsp`-based addresses count as the stack; heap pointers in `%rbp` no
  longer hide loads and stores.
- The source lint reads every file under the solver directory and Cargo build
  scripts, and no longer refuses `#pragma once` or a C function named `target`.
- The answer check tells a crash, a nonzero exit, and a timeout apart.
- 12 Python stubs (03, 18, 19, 21, 22, 24–26, 28, 36, 42, 44) failed ruff lint
  before their tests ran; ruff is pinned to 0.16.9 in every Makefile.
- `scripts/test_bench.py` no longer fails under load on child start-up.

### Changed

- A failed `make vec` lists the five places with the most scalar work, by
  source line.
- The vec READMEs state the budget as a bare total and say which intrinsics a
  `solve` may use in C, Rust, and Go; they no longer describe the work's shape.
- Hint 1 of 13, 44, and 46 is a question; the named technique moved to hint 2.
- Go solver builds go inside their directory, not a shared `/tmp` path.
- C `make help` lists `vec`; 66–68's C directories drop the `bench` rule.
- 13's C `solve` takes the readings as `int32_t`, like golden, Rust, and Go.
- Hint figures re-measured under the new grader.

### Added

- A larger small case for 17, 44, and 46, and a third 59 large recipe where
  most days are never undercut.

## [v0.1.7] — 2026-09-26

> challenges v0.1.7 — three levels: correct, fast, vectorized
>
> Four existing challenges gain a third level: after passing `make test` and
> `make bench`, `make vec` checks that `solve` really runs in SIMD lanes.
>
> • 13, 17, 44, 46 get `make vec` in C, Rust, and Go; 66–68 stay vec-only
> • `make vec` refuses threads, crashes, and hangs, and checks every answer
> • Bigger large cases, so a naive loop at `-O3` still times out
> • 44's reference fixed: it scored some gap-after-gap alignments wrong
>
> Full notes below.

### Added

- **vec level** for io challenges 13, 17, 44, and 46: `make vec` in their C,
  Rust, and Go solver directories, after `make test` and `make bench`.
  Their READMEs gain a Level 3 section and their hints level-3 rungs.
- `make vec` first checks the traced build's answer on every case and on the
  traced fixture.
- `VEC_UNITS` takes a product such as `items*capacity`.
- Small cases for 13 (10–18), 44 (10), and 46 (10–11).

### Changed

- 13, 17, 44, and 46's `golden/` is the vectorized C reference and the
  `make bench` oracle; `rotten/` stays Python. The root `make test`,
  `make golden`, and `make vec` cover C goldens.
- Every target of a vec challenge's C, Rust, and Go solver directories builds
  for `x86-64-v3`, so `make test`, `make bench`, and `make vec` check one program.
- 13's Go `solve` takes the readings as `[]int32`.
- Larger large cases, which a naive loop at `-O3 -march=x86-64-v3` cleared in
  under 5 s: 13 has `n = 10⁶` (limit raised from 2·10⁵), 44 up to 2500 residues
  (limit raised from 2000), and `46_large_many` guides of 20 bases.
- The README explains the three levels once; the catalog lists each
  challenge's levels.
- The root Makefile keeps each check's output in memory, not in `/tmp` files
  that runs in other checkouts overwrite.

### Fixed

- `make vec` refuses a `solve` that starts a thread, a process, or a
  goroutine, whose work it did not trace.
- `make vec`'s answer check fails a build that exits nonzero or runs past
  10 s, where it passed or hung.
- C solver builds rebuild when their Makefile changes, such as a new flag.
- 44's `c/` builds without gcc's loop distribution, which at `-O3` in gcc 12.2
  gave wrong answers for a correct row-by-row `solve`.
- 44's golden opened a gap only after a match, so it missed alignments that put
  a gap in `t` right after a gap in `s`; `W`×11 against `D`×11 scored -44
  instead of -42.

## [v0.1.6] — 2026-09-26

> challenges v0.1.6 — SIMD-graded challenges
>
> Three new challenges check how your code computes the answer, not only the
> answer: the hot loop must run in SIMD lanes.
>
> • 66–68 (Variant Allele Counts, Tick Frame Audit, Sparse Activation Gate)
> • `make vec` traces `solve` and fails a solve that does per-element scalar work
> • Solve them in C, Rust, or Go — Go may use the new `simd/archsimd` package
> • Every Go module moves to Go 1.27.1
>
> Full notes below.

### Added

- **vec challenge type**, challenges 66–68: C `golden/` and `rotten/`
  controls, `cases/`, `hints/`, and `c/`, `rust/`, `go/` solver scaffolds.
  Root `make vec` checks every golden vectorizes and every rotten stays
  scalar, under `cc` and also `clang` when it is on PATH.
- `scripts/vec_check.py`: a ptrace tracer that single-steps `solve` and its
  callees and passes under one scalar instruction per input element. It
  refuses assembly, pragmas, target/optimize attributes, `#[target_feature]`,
  `build.rs` and cgo, stops at AVX-512, and does not count Go runtime stack
  growth, heap growth, or preemption. Hangs end after 60 seconds.
- Go track for 66–68 (`GOEXPERIMENT=simd`, `GOAMD64=v3`); Rust tests and grades
  one release `x86-64-v3` build.

### Changed

- Merged v0.1.5; the vec challenges moved from 58–60 to 66–68 and took
  solution-neutral slugs.
- Every Go module and the template declare `go 1.27.1`.
- README and CLAUDE.md count 67 challenges and drop the retired quiz type;
  NOTICE points to `hints/`.

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
