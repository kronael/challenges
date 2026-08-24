# Defect log

## Status — 2026-08-22 — README novice-clarity editorial pass (01-65 + root)

Single-voice prose/clarity pass over every challenge `README.md` plus the
root `README.md`. Light touches only (spelled-out `i32`/`i64` → "signed
32/64-bit integer" in 09, 10, 13, 25, 28, 41, 43; a couple of missing-gloss
and thin-example fixes) were made directly and are not repeated here — see
the diff. The three items below are judgment calls or pre-existing issues
outside this pass's prose-clarity scope, left for the owner.

- **DOC-HEADER-MISSING-METADATA** (LOW, docs) — `49-hard-gene-region-decoder`,
  `50-hard-tree-sequence-likelihood`, `51-hard-deadline-scheduler`, and
  `52-hard-service-pairing` (all four from the same "research-backed hard
  exercises" commit) each skip the `**Task**:`/`**Difficulty**:`/`**Time
  estimate**:` header and `## Problem` heading that every other challenge
  README uses, and use `## Example` (singular) plus ```` ```text ```` Run
  fences instead of the majority convention. Not fixed here: a `**Time
  estimate**` value is a judgment call belonging to the owner, not something
  to fabricate during a prose pass. **Fix:** add the standard header once the
  owner supplies (or approves) a time estimate for each.
- **55-README-OFFLINE-HINT** (LOW, solution-neutrality) —
  `55-hard-changing-network-queries/README.md`'s "The full operation sequence
  is available before processing begins" telegraphs that an offline approach
  is intended; `hints/01.md` confirms that's exactly the technique (a
  segment tree over operation indices). Pre-existing text, not touched
  during this pass — fixing it is a spec-wording change that needs owner
  sign-off, not a unilateral edit. **Fix:** reword to state the constraint
  (e.g. batch input) without foreshadowing offline-vs-online processing, or
  accept it as within the bare-constraint allowance.
- **56-README-COLLINEAR-AMBIGUOUS** (LOW, docs) —
  `56-hard-orthogonal-segment-crossings/README.md`: "Collinear pairs are not
  part of the count" is unclear, since a horizontal segment (`y` fixed) and a
  vertical segment (`x` fixed) are perpendicular by construction and it's not
  obvious what a "collinear" horizontal/vertical pair would even be (a
  degenerate zero-length segment lying along the other's line, perhaps).
  Left unedited: clarifying it risks stating something wrong about the
  actual excluded case, which needs a correctness check against `golden/`
  rather than a guess during a prose pass. **Fix:** owner clarifies the
  excluded case in one clause once confirmed against `golden/`.

## Status — 2026-08-22 — adversarial review of challenges 58-63

Deep review of the six brand-new challenges (58-63), the hints/ schema, the
24-medium-lru-cache fix, and the CLAUDE.md bare-target-complexity exception,
using four parallel read-only reviewers plus independent hand/native-control
verification. Confirmed bugs (stale hint references, wrong numbers, an
off-by-one in an off-by-one lesson, a large-case recipe that violated its own
README's `n` bound, a solution-neutrality violation in 58's follow-up line,
missing README fixture/blockquote parity) were fixed directly and are not
repeated here — see the diff. These are the judgment calls that need
product-level buy-in rather than a unilateral fix.

- **59-BENCH-MARGIN-THIN** (MED, bench) — `rotten/main.py`'s bench margin
  against the 5 s Rust/Go/C timeout is only 3.2x under the repo's own
  `-O2` flags (measured 15.8 s) and collapses to 2.46x under
  `-O3 -march=native` (`shared/c/io.mk:3` declares `CFLAGS ?= ...`, so a
  solver can override it), the thinnest margin of the six new challenges.
  Not broken at the flags the repo actually uses, but the thinnest wall here.
  **Fix:** raise `n`'s cap (e.g. 500000, ~63 s at `-O2`) or accept and note
  the flag sensitivity in `hints/04.md`.
- **59-RECIPE-NO-WORST-CASE-GUARANTEE** (LOW, bench) — both of
  `59-medium-price-undercut`'s seeded large recipes
  (`scripts/large_cases.py`, `build_59`) are non-decreasing with a single
  terminal drop, so a skip-ahead heuristic with no worst-case guarantee
  solves both in linear time; `hints/03.md` admits this honestly but nothing
  enforces it. **Fix:** a third recipe with a shape that defeats the
  heuristic (needs a digest refreeze).
- **60-BENCH-DOESNT-EXERCISE-WORST-CASE** (MED, bench) — `README.md:33` caps
  `q` at 5000, and `hints/03.md`'s "`q` is at most 5000, so the plain climb
  is what the limits ask for" is only true of the *shipped* recipes
  (0.042 s / 0.148 s intended-algorithm time). A fully legal input at the
  stated limits (n=200000, one root, q=5000, a deep two-armed tree) pushes
  the intended O(depth) climb to ~5.04 s against the 5 s timeout — the
  benchmark exercises roughly 1-3% of the advertised worst case. **Fix:**
  lower `q`'s cap, bound depth, or reword `hints/03.md:33-34` to say the
  *benchmark* doesn't create that case rather than the *limits* don't.
- **60-TITLE-LEAKS-TERM** (LOW, design) — `README.md:1`'s title "Venue
  Ancestor" and the directory slug name the classic LCA problem, while the
  body (`README.md`) works to avoid ever saying "ancestor". Defensible per
  CLAUDE.md:109 ("names are part of the prompt", and "ancestor" names the
  problem not the method) but an asymmetry with 61, whose slug/title use its
  own README-defined term ("critical") and never leak "bridge". **Fix:**
  none needed unless the owner wants the circumlocution in the body dropped
  to match the title, or the title softened to match the body.
- **60-HINT-PACING-RUNGS-COLLAPSED** (LOW, design) — `hints/01.md:15` poses
  "What would you need to know about each venue before a lockstep walk makes
  sense?" and answers it two lines later at `hints/01.md:17` ("Level them
  first..."), so hint 1 both asks and answers in one file rather than leaving
  the answer for hint 2, unlike 59's gradient. **Fix:** move the
  "Level them first" paragraph to the top of `hints/02.md` and let `01.md`
  end on the question — cosmetic pacing, not a factual error, left as-is
  pending owner preference.
- **59-HINTS-APPROACH-ORDER-VARIANCE** (LOW, docs) — `59-medium-price-undercut`
  titles `hints/02.md` "Approach" and only rejects alternatives in
  `hints/03.md`, while `58` and `60` fold both into one "Approach — why the
  two obvious tools/alternatives are wrong here" file. Direct review found
  59's resulting chain "genuinely progressive" regardless, so this is a
  file-title/order labeling variance, not a comprehension problem. **Fix:**
  none needed; note only for anyone standardizing the hints/ skeleton later.
- **58-HINT-CHAIN-RUNGS-COLLAPSED** (LOW, design) — `58-medium-kth-worst-fill/hints/01.md:10`
  names Quickselect and prescribes the full loop in the first hint file, and
  `hints/03.md:1` ("Approach — why the two obvious tools are wrong here") is
  the rejected-approaches file rather than a distinct approach step, so the
  chain has no separate "Approach" rung the way 59's does. **Fix:** none
  applied; 59's 01/02/03 split is the model if the owner wants it matched.
- **58-BENCH-REWARDS-SORT-ON-SEEDED-RECIPES** (LOW, bench) — on
  `58-medium-kth-worst-fill`'s two seeded large recipes specifically,
  Python's built-in `sorted()` (0.209 s / 0.035 s) beats `golden/main.py`'s
  quickselect (715 ms). This is exactly why the README states a bare O(n)
  time / O(1)-space follow-up rather than relying on `make bench` (per the
  tightened CLAUDE.md exception clause), and `hints/04.md` now says so
  explicitly — but a solver who only watches the clock, ignoring the
  follow-up, is rewarded for violating it on these particular inputs.
  **Fix:** none further applied; a recipe shaped to also punish a full sort
  would need a digest-changing addition to `scripts/large_cases.py`, owner's
  call.
- **62-HINT-01-STRONG-SPOILER** (LOW, design) — `62-hard-neutral-basket/hints/01.md`
  rules out both brute force and a sum-indexed DP and hands the solver
  `2^19` in the first file, more than any sibling's hint 1 gives away.
  Defensible for a `n <= 38` problem with only two live options, but the
  owner may want a gentler hint 1 with the halving pushed to hint 2.
  **Fix:** none applied; owner's call.
- **62-SMALL-FIXTURE-COVERAGE-GAP** (LOW, test) — the largest tracked small
  fixture in `62-hard-neutral-basket/cases/` is `n=17` (forced: `rotten`
  must still pass the small suite quickly, and `n=20` already costs ~4 s of
  rotten's Python runtime), so the `middle = 19/19` split path is exercised
  only by `make bench`, never by the tracked small suite. **Fix:** none
  applied — raising a small fixture to `n=19` risks slowing `rotten`'s test
  target; owner's call on the trade-off.
- **63-HINT-MARGIN-HARDWARE-DEPENDENT** (LOW, bench) — `hints/04.md:76-77`
  claims "a margin of roughly 10x for the fastest native brute force"; this
  is internally consistent with the table's own authored numbers (81 s/49 s)
  but a faster reviewer machine measured 62.61 s/35.68 s for the same
  control, i.e. as low as ~7.1x on the tighter recipe. The wall itself is
  real and not closed by any plausible scalar rewrite — only a deliberately
  vectorized backward scan could plausibly approach the timeout — but the
  specific multiplier is machine-dependent. **Fix:** none applied (changing
  the number to match one box could make it wrong on another); reword to a
  qualitative "roughly an order of magnitude" if the owner wants it
  hardware-robust.

## Status — 2026-08-22 — hints/ migration + structural alignment sweep (57 challenges)

Found while migrating every `HINTS.md` to per-hint `hints/NN.md` files across
challenges 01-57 (4 parallel buckets: 01-14, 15-28, 29-42, 43-57 — 57 challenges,
not 58; the bucket list undercounts because 43-57 is 15 wide) plus a
separate LRU-cache deep audit. Challenges 58-63 did not exist yet at sweep time
and are covered by the newer block below. Record-only per triage — hint
migration itself is done and verified (all golden/rotten tests still pass);
these are things noticed along the way, not blockers.

- **DOC-API-2122-GOLDEN-MISMATCH** (LOW, docs) — `CLAUDE.md`'s Layout section
  claims challenges 21/22 have only `python/`+`go/`, but both have a tracked
  `golden/` (`main.py`, `Makefile`, `pyproject.toml`, `test_solution.py`).
  **Fix:** update the CLAUDE.md note, or remove the golden dirs if stale.
- **22-GOLDEN-TEST-NO-VALUE-CHECK** (MED, test) —
  `22-medium-unbounded-sequences/golden/test_solution.py` only asserts function
  names exist and signatures match the README (`inspect.signature`); it never
  checks actual output values, unlike `21/golden/test_solution.py`'s 8
  value-checking tests. Golden's correctness there is unverified by its own
  suite. **Fix:** add real value-checking tests to 22's golden.
- **SYS-2934-MAKEFILE-DRIFT** (LOW, config) — across sys challenges 29-34: (a)
  `help` targets in c/go/rust Makefiles never list `check`/`help` themselves;
  (b) 29/30/34's `go/Makefile` help text says "(small cases only)" though sys
  challenges have no cases; (c) 30 and 34's golden/rotten Makefiles hardcode
  `cc` while 29/31/32/33 use `CC ?= gcc`; (d) 31/32's rust Makefile bench
  charges a cold `cargo build --release` compile against the 5s TIMEOUT budget
  while 29/30/33/34 build first then time; `TIMEOUT` is bare `5` in some, `5s`
  in others, and 31's Makefile declares `TIMEOUT ?= 5s` on the line *after*
  it's already used. **Fix:** standardize CC/TIMEOUT/help text across the six
  sys Makefiles.
- **41-STRAY-RUFF-CACHE** (LOW, resource) —
  `41-hard-ordered-set-queries/.ruff_cache/` sits at the challenge root
  (gitignored, uncommitted) instead of inside a language dir — the only such
  case repo-wide. **Fix:** delete (non-recursive removal per repo rules — needs
  explicit approval or manual cleanup).
- **37-RUST-ACCESSOR-INCONSISTENT** (LOW, design) —
  `37-hard-prime-pair-sets/rust/src/lib.rs` adds `Input::size()/limit()`
  accessor methods over already-public fields; every sibling stub reads fields
  directly. **Fix:** drop the accessors, or leave as harmless variance.
- **SYS-CARGO-ARTIFACTS-NOT-CLEANED** (LOW, ops) — all six sys challenges
  (29-34) leave an untracked `rust/Cargo.lock`; `cargo clean` doesn't remove it
  and root `make clean` doesn't cover sys rust dirs for this file. **Fix:** add
  lockfile + build artifacts to gitignore/clean targets.
- **DOC-README-SECTION-HEADING-DIVERGENCE** (LOW, docs) —
  `template/README.md` uses `## Constraints`, `## Example` (singular), and a
  closing "No debug prints" blockquote that essentially no real challenge
  follows: 43-48 use `## Examples` (plural) while 49-57 use singular; 49-52
  have no `## Problem` heading at all; all of 01-58 fold constraints into
  inline prose rather than a `## Constraints` heading (matching hardened
  exemplars 08/14/24/25, which already diverged from the template first).
  **Fix:** decide which side is canonical — the template is currently the
  outlier, not the challenges.
- **DOC-ASCII-LTE-GLYPH-INCONSISTENT** (LOW, docs) —
  `53-hard-circular-genome-distance/README.md:23`,
  `55-hard-changing-network-queries/README.md:22`,
  `56-hard-orthogonal-segment-crossings/README.md:19` use ASCII `<=` where 13+
  sibling READMEs use `≤` and `·10ⁿ` notation (e.g.
  `45-hard-kmer-assembly/README.md:24`). **Fix:** swap in the `≤` glyph.
- **04-SLUG-TITLE-MISMATCH** (MED, docs) — `04-medium-edge-costs`'s README
  title and catalog row say "Vertex Load Assignment," and the problem assigns
  loads to vertices over unit edges — the slug "edge-costs" matches neither
  the title nor the actual problem. Not renamed: would break catalog links and
  the `04_large_*` recipe names in `scripts/large_cases.py`. **Fix:** needs a
  coordinated rename across README, catalog row, and large_cases.py recipe
  names if ever done — record-only for now.
- **10-HINTS-NO-COMPLEXITY-CONTENT** (LOW, docs) —
  `10-medium-route-costs`'s original `HINTS.md` never had a trailing
  naive/rotten-timeout paragraph (unlike all 13 siblings in its migration
  bucket), so its `hints/` has no Complexity file naming `rotten/main.py`; the
  O(n²) point is made only abstractly in Hint 3. **Fix:** add a Complexity file
  naming the actual rotten trap.
- **45-HINTS-COMPLEXITY-NO-ROTTEN-NAME** (LOW, docs) —
  `45-hard-kmer-assembly/hints/06.md` describes the naive baseline without
  ever naming `rotten/`, unlike all other Complexity files in 43-57. **Fix:**
  name the file explicitly for solver clarity.
- **07-HINTS-SOURCES-VAGUE-CITATION** (LOW, docs) —
  `07-medium-coin-change/hints/05.md`'s Sources file is a bare "CLRS" with no
  section number, unlike siblings citing precise sections (§4.1, §31.6, etc).
  **Fix:** add the specific CLRS section.

## Status — 2026-08-11 — Go numeric-width sweep

- **03-GO-DRAWDOWN-INT-RESULT** (HIGH, correctness) — The documented drawdown
  is signed 64-bit, but `03-easy-max-drawdown/go/main.go:14` and
  `go/solution_test.go:43` use `int`; valid i32 prices can produce
  `4294967295`, which overflows on GOARCH=386. **Fix:** Return and parse `int64`,
  widening operands before subtraction.
- **04-GO-LOADS-INT-NARROWING** (HIGH, correctness) — Loads are signed 64-bit,
  but `04-medium-edge-costs/go/main.go:13` parses them through `*int` and
  `go/solution_test.go:50` expects `[]int`; GOARCH=386 rejects a valid load of
  `2147483648`. **Fix:** Use nullable `int64` loads and `[]int64` results.
- **07-GO-COINS-INT-NARROWING** (MED, correctness) — Denominations have no
  upper bound, but `07-medium-coin-change/go/main.go:11` parses them as `int`;
  GOARCH=386 rejects a valid denomination of `2147483648`. **Fix:** Either give
  denominations a meaningful documented bound or widen their Go type.
- **10-GO-WEIGHTS-INT-NARROWING** (HIGH, correctness) — Edge weights are
  nonnegative and only bounded by the i64 distance contract, but
  `10-medium-route-costs/go/main.go:11` parses all edge fields as `int`;
  GOARCH=386 rejects a valid weight of `2147483648`. **Fix:** Use typed edges
  with bounded `int` endpoints and `int64` weights.
- **17-GO-VALUE-TOTAL-INT-NARROWING** (HIGH, correctness) — Results and
  accumulated values are signed 64-bit, but
  `17-medium-knapsack/go/main.go:11,19` and `go/solution_test.go:43` use `int`;
  existing case 11 expects `6442450941`. **Fix:** Use `int64` for values,
  results, accumulation, and expected-output parsing.
- **35-GO-OP-VALUE-INT-NARROWING** (HIGH, correctness) — Initial values and
  assignments are signed 64-bit, but `35-hard-dynamic-range-sums/go/main.go:13`
  stores the mixed operation operand in `int`; GOARCH=386 rejects a valid
  assignment of `2147483648`. **Fix:** Keep positions bounded and represent the
  assignment payload as `int64`, matching challenge 26's scaffold pattern.
- **42-GO-QUERY-ENDPOINT-INT-NARROWING** (MED, correctness) — Raw query
  endpoints are clamped and have no bound, but
  `42-hard-fragmented-string-queries/go/main.go:11` decodes them into `int`;
  GOARCH=386 rejects `2147483648` before clamping. **Fix:** Parse endpoints as
  `int64` and convert only after clamping to the bounded string length.
- **43-GO-BOOK-QUANTITY-INT-NARROWING** (HIGH, correctness) — Individual
  quantities fit i32, but final price-level totals need not; the `[]int` result
  at `43-hard-order-book/go/main.go:23` and `Atoi` at
  `go/solution_test.go:45` overflow for two valid maximum-size orders totaling
  `4294967294`. **Fix:** Use `int64` for aggregate quantities, results, and
  expected-output parsing.
- **47-GO-MIN-LOOP-INT-NARROWING** (MED, correctness) — `min_loop` is
  nonnegative but unbounded, while `47-hard-rna-max-pairs/go/main.go:11` uses
  `int`; GOARCH=386 rejects `2147483648` although it has a well-defined zero
  result. **Fix:** Add a meaningful upper bound or widen the parsed type.
- **54-GO-MASS-INT-NARROWING** (MED, correctness) — Allowed masses are positive
  integers without an upper bound, but
  `54-hard-spectrum-peptide-recovery/go/main.go:12` uses `[]int`; GOARCH=386
  rejects a valid unmatched mass of `2147483648`. **Fix:** Bound masses to the
  parent-mass domain or use `int64` consistently with the C and Rust tracks.
- **57-EVENT-ID-INT-NARROWING** (HIGH, correctness) — Event IDs have no bound;
  Go uses `int` at `57-hard-causal-event-replay/go/main.go:12,22` and C uses
  `int` at `c/solution.h:10`, while Rust and the C answer use 64-bit IDs.
  GOARCH=386 rejects `2147483648`. **Fix:** Make IDs signed 64-bit end to end,
  including output parsing.
- **01-INT64-ELEMENT-BOUNDARY-UNTESTED** (LOW, test) — Values are signed
  64-bit at `01-easy-max-subarray/README.md:13`, but every fixture element fits
  i32; the existing large output tests accumulation only. **Fix:** Add a small
  fixture with an element outside signed 32-bit.
- **02-INT64-OUTPUT-BOUNDARY-UNTESTED** (LOW, test) — Inputs reach `10^18` as
  allowed by `02-easy-mod-exp/README.md:15`, but no expected output exceeds
  signed 32-bit. **Fix:** Add a case with a valid result above `2147483647`.
- **28-INT64-EVENT-BOUNDARY-UNTESTED** (LOW, test) — Timestamps and IDs are i64
  at `28-medium-news-feed-merge/README.md:17`, but all fixture values are at
  most `500000`. **Fix:** Add a small ordering case outside signed 32-bit.
- **49-INT64-SCORE-TOTAL-UNTESTED** (LOW, test) — Best totals may be signed
  64-bit at `49-hard-gene-region-decoder/README.md:32`, but fixtures use scores
  only from `-12` to `12` and short sequences. **Fix:** Add a case whose path
  total crosses signed 32-bit.
- **52-INT64-COST-TOTAL-UNTESTED** (LOW, test) — Minimum totals may be signed
  64-bit at `52-hard-service-pairing/README.md:16`, but fixtures stay between
  `-15` and `197`. **Fix:** Add a small matrix whose minimum crosses signed
  32-bit.
