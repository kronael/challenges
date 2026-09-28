# Defect log

Review queue: **OPEN / DEFERRED / BY-DESIGN only.** Resolved bugs live in git
history and `CHANGELOG.md`, not here.

## Status — 2026-08-24 — defect-queue resolution pass (toward v0.1.5)

Worked the full queue from the earlier audits. The correctness and consistency
items were FIXED and pruned from this file — they live in the v0.1.5 commits and
`CHANGELOG.md`. Fixes verified end to end (`make test`, `make cases`, `make sys`,
`make sys-rotten`, per-language `go build`/`vet`, golden+rotten suites) and
independently reverified by an Opus pass (README solution-neutrality, the 56
collinear removal, the 22 golden value tests) and a Sonnet numbering/reference
sweep (hint chains + case pairing).

Pruned as FIXED this pass: the eleven Go int-narrowing scaffolds (03, 04, 07, 10,
17, 35, 42, 43, 47, 54, 57 — plus 57's C `Event.id`), the five int64-boundary
fixtures (01, 02, 28, 49, 52), the sys 29–34 Makefile standardization and
`Cargo.lock` cleanup, the 22 golden value tests, the 37 Rust accessor removal,
the CLAUDE.md 21/22 note, the template heading alignment, the ≤/superscript glyph
fixes (53/55/56), the 55 offline-hint and 56 collinear rewordings, the 49–52
README headers, the 07/10/45 hint-source/complexity touch-ups, and the 59/60/63
benchmark-margin wording.

What remains below is BY-DESIGN (accepted variance).

### By design — accepted variance, no change

- **60-TITLE-LEAKS-TERM** (LOW, design) — BY-DESIGN. `60-medium-venue-ancestor`'s
  title/slug name the classic LCA problem while the body avoids "ancestor."
  Defensible per CLAUDE.md ("names are part of the prompt"; "ancestor" names the
  problem, not the method).
- **60-HINT-PACING-RUNGS-COLLAPSED** (LOW, design) — BY-DESIGN. `hints/01.md`
  poses and then answers its lockstep-walk question inside one file. It still
  ends on a distinct cliffhanger (filling the depth array without deep
  recursion), so the chain stays progressive.
- **59-HINTS-APPROACH-ORDER-VARIANCE** (LOW, docs) — BY-DESIGN. 59 titles
  `hints/02.md` "Approach" and rejects alternatives in `03.md`, where 58/60 fold
  both together. A file-title labeling variance; the chain is progressive.
- **58-HINT-CHAIN-RUNGS-COLLAPSED** (LOW, design) — BY-DESIGN. 58's hint 1 names
  the selection method and `03.md` is the rejected-approaches file, so there is
  no separate "Approach" rung. Design variance, not a factual error.
- **62-HINT-01-STRONG-SPOILER** (LOW, design) — BY-DESIGN. `62-hard-neutral-basket`'s
  hint 1 rules out brute force and a sum-indexed DP and hands the solver `2^19`,
  but defers *what* there are `2^19` of to hint 2 — appropriate escalation for
  an `n ≤ 38` problem with only two live options.
- **VEC-UNROLLED-STACK-LANES** (LOW, grading) — BY-DESIGN. `scripts/vec_check.py`
  counts no stack access, and no general-purpose arithmetic inside a vector
  iteration, one that runs a packed instruction or loads several elements into
  a vector register, because that is where Go spills and where every language
  keeps its per-vector loop control, bounds checks, and mask arithmetic. A
  `solve` that copies a block to a local array, runs one packed instruction on
  it, and handles each lane with scalar code unrolled inside that same
  iteration therefore grades vectorized. A heap load or store counts only when
  it moves one element: a vector block move, such as a 32-byte `memcpy`,
  counts on neither side. So 68's C that copies 8 scores to the stack, compares
  them with one `_mm256_cmpgt_epi32`, stores each lane at a running index from
  the mask bits, and copies the block out grades `0.01 scalar, 0.25 packed ->
  vectorized` (2026-09-26); without the packed compare it has 0.00 packed and
  grades scalar. Every separate scalar pass and every scalar floating-point add
  still counts. **Fix (optional):** tell apart stack slots that hold spilled
  vectors, which needs data flow the tracer does not track.
- **VEC-WORK-BEFORE-SOLVE** (MED, grading) — BY-DESIGN. `scripts/vec_check.py`
  traces only `solve`, so work the program does before `solve` is entered is
  not graded. The solver edits the code that runs then: C's `input_parse` lives
  in `solution.c`, a C `__attribute__((constructor))` or a Go `init` runs
  before `main`, and Rust's `src/main.rs` and Go's `main.go` sit beside the
  edited file. Any of them can compute the answer for `solve` to copy out, or
  start a thread or process that finishes it before `solve` starts; the grader
  stops other threads and refuses other processes only from `solve`'s entry.
  Owner's ruling (2026-09-27): not worth a contract change; the level does not
  police work done outside `solve`.
- **16-LIBRARY-COMPARE-CLEARS-BENCH** (MED, design) — BY-DESIGN.
  `16-medium-string-search`'s wall holds only against the character by
  character loop in `rotten/main.py:6`. The same O(|T|·|P|) scan written with a
  library compare clears `make bench` at the README maximum: C `memcmp` takes
  0.5–0.8 s CPU a case, Python `text.startswith(pattern, i)` at most 1.5 s, and
  a 2× wall against `memcmp` needs |T|·|P| about 15× larger (measured
  2026-09-27). Owner's ruling (2026-09-28): the README's bare O(|T| + |P|)
  time follow-up now carries the requirement; `make bench` times only the
  character loop.
- **58-BENCH-REWARDS-SORT-ON-SEEDED-RECIPES** (LOW, bench) — BY-DESIGN. On
  `58-medium-kth-worst-fill`'s two seeded recipes, a full `sorted()` beats the
  intended selection; the README's bare O(n) time / O(1)-space follow-up
  carries the requirement instead of `make bench`, and `hints/04.md` says so.
  Owner's ruling (2026-09-28): accepted; no recipe shaped to punish a sort.
- **62-SMALL-FIXTURE-COVERAGE-GAP** (LOW, test) — BY-DESIGN. The largest tracked
  small fixture in `62-hard-neutral-basket` is `n=17`; the `middle = 19/19`
  split path is exercised only by `make bench`, because `n=20` already costs
  ~4 s of `rotten`'s Python runtime in the small suite. Owner's ruling
  (2026-09-28): accepted; the small suite stays fast.
- **46-BENCH-WALL-UNDER-2X** (LOW, design) — BY-DESIGN. A native control of
  `rotten/` (guide × window × base, `-O3 -march=native`) takes 7.7 s CPU a case
  on both recipes, 1.54× the 5 s budget. A 2× wall needs about 1.3·10⁶ bases,
  where the Go sliding window of `hints/06.md` stops fitting the budget, and
  the same triple loop with the window loop innermost vectorizes to 1.0 s a
  case (golden 0.9 s), so no genome length separates it from the golden
  (measured 2026-09-27). Owner's ruling (2026-09-28): accept the 1.5× wall and
  the swapped-loop pass.
- **41-RANGE-WALL-UNDER-2X** (LOW, design) — BY-DESIGN. `10_large_range`
  (3·10⁵ inserts, then 5·10⁴ narrow range counts) holds a native control of
  `rotten/` to 8.7 s CPU at `-O3 -march=native`, 1.74× the 5 s budget, while
  the Python golden spends about 10 µs an operation (3.1 s), so no mix within
  a third of the 10 s Python timeout reaches a 2× wall (measured 2026-09-27).
  Owner's ruling (2026-09-28): accept the 1.74× wall.
- **CASE-NUMBER-BANDS** (LOW, test) — BY-DESIGN. Case-number bands like
  `58/13_i32_bounds.in` and `04/12–20.in` are intentional: every `.in` is
  paired and each challenge has ≥8 small cases.

## vec grader

- **VEC-LINT-TEXT-ONLY** (LOW, hardening) — Record-only, no sound fix for the
  remainder. `lint()` in `scripts/vec_check.py` reads only the solver
  directory, so it cannot see the code of a Cargo or Go dependency the build
  pulls in and compiles: the assembly, target pragma, or build script the
  solver's own files may not carry can live in a dependency instead. Closing
  it means vendoring and scanning the whole dependency graph, or trusting it —
  out of scope. The in-directory escapes the entry once listed are now refused:
  the C is scanned after `cc -E` (so token-pasted keywords, macro-named
  attributes, and trigraph/digraph pragmas are seen post-expansion, and an
  outside `#include` is scanned wherever it resolves while `<...>` system
  headers stay exempt), and `include!`/`#[path]`/Cargo `[lib] path`/Go
  `replace` reaching outside, a `.cargo/config`, and a solver Makefile
  overriding a `shared/c/io.mk` or `shared/vec.mk` recipe are refused.
