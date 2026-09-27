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

What remains below is DEFERRED (needs a frozen-digest change or an owner naming
decision) or BY-DESIGN (accepted variance).

### Deferred — need a spec/digest decision or coordinated rename

- **04-SLUG-TITLE-MISMATCH** (MED, docs) — DEFERRED. `04-medium-edge-costs`'s
  README title and catalog row say "Vertex Load Assignment," and the problem
  assigns loads to vertices over unit edges — the slug "edge-costs" matches
  neither. **Fix:** a coordinated rename across the directory slug, README,
  catalog row, and `scripts/large_cases.py` recipe context (owner picks the
  canonical name first).
- **58-BENCH-REWARDS-SORT-ON-SEEDED-RECIPES** (LOW, bench) — BY-DESIGN. On
  `58-medium-kth-worst-fill`'s two seeded recipes, a full `sorted()` beats the
  intended selection. This is exactly why the README states a bare O(n)
  time / O(1)-space follow-up rather than leaning on `make bench`, and
  `hints/04.md` says so. **Fix (optional):** a recipe shaped to also punish a
  full sort (digest refreeze).
- **62-SMALL-FIXTURE-COVERAGE-GAP** (LOW, test) — DEFERRED. The largest tracked
  small fixture in `62-hard-neutral-basket` is `n=17`; the `middle = 19/19`
  split path is exercised only by `make bench`, because `n=20` already costs
  ~4 s of `rotten`'s Python runtime in the small suite. **Fix:** owner's call on
  the rotten-runtime trade-off.
- **11-INPUT-KEY-NAMES-METHOD** (LOW, docs) — DEFERRED, needs sign-off.
  `11-medium-friend-groups`'s input key `unions` (README.md:27, every
  `cases/*.in`) names the merge operation of the structure the hints teach,
  while the README prose says "friendships"; CLAUDE.md counts names as part of
  the prompt. The key is read by golden, rotten, all four solver scaffolds, and
  `scripts/large_cases.py`. **Fix:** a coordinated rename (e.g. `friendships`)
  across those files and the README, with a digest refreeze. Found 2026-09-26.
- **22-API-NAME-SIEVE** (LOW, docs) — DEFERRED, needs sign-off.
  `22-medium-unbounded-sequences` asks for `sieve(nums)` / Go `Sieve`
  (README.md:18), which yields the primes among an ascending stream; the name
  states the method for doing it. The name is fixed by `python/main.py`,
  `go/solution.go`, both test suites, golden, and `hints/02.md`. **Fix:** owner
  rules it by design (the classic name of the exercise) or renames it (e.g.
  `keep_primes`) across those files. Found 2026-09-26.
- **41-STRAY-RUFF-CACHE** (LOW, resource) — DEFERRED. `41-hard-ordered-set-queries/.ruff_cache/`
  sits at the challenge root instead of inside a language dir. It is gitignored,
  so it never reaches git and does not block a release. **Fix:** manual cleanup
  — repo policy bars recursive removal, so it is left for the owner.

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

## Status — 2026-08-24 — found during the numbering/reference sweep

- **HINTS-MISSING-SOURCES-FILE** (LOW, docs) — Record-only. Thirteen challenges'
  `hints/` end with a `# Complexity` file and have no `# Sources` file at all:
  03, 04, 09, 14, 15, 16, 23, 24, 25, 35, 38, 39, 43. CLAUDE.md says a hint
  chain ends with a Sources file holding solution-bearing attribution. Several of
  these are classic problems with citable sources (e.g. 24 LRU cache, 14 sieve,
  25 running median); others may be original and legitimately source-less.
  **Fix:** owner decides per challenge — add an accurate Sources file where a
  real citation exists, or accept Complexity-last for genuinely source-less
  problems. Do NOT fabricate citations. (Case-number bands like `58/13_i32_bounds.in`
  and `04/12–20.in` were also reviewed and are intentional/harmless — every
  `.in` is paired and each challenge has ≥8 small cases — so they are not logged.)

## make bench walls

- **16-LIBRARY-COMPARE-CLEARS-BENCH** (MED, design) — needs sign-off.
  `16-medium-string-search`'s wall holds only against the character by
  character loop in `rotten/main.py:6`. The same O(|T|·|P|) scan written with a
  library compare clears `make bench` on both recipes at the README maximum
  (|T| = 3·10⁶, |P| = 1.5·10⁴): C `memcmp` takes 0.5–0.8 s CPU a case at `-O2`
  and `-O3 -march=native`, and Python `text.startswith(pattern, i)` takes 1.5 s
  on `09_large_allmatch` and 0.17 s on `10_large_nearmiss`, where CPython
  compares the last character first. Rust slice `==` and Go string `==` reach
  the same library compare (not timed). The character loop in C takes 11.7 s
  at `-O2`. A 2× wall against `memcmp` needs |T|·|P| about 15× larger, and
  the golden already prints 3·10⁶ positions on allmatch. **Fix:** owner's call —
  a bare time bound in the README (the CLAUDE.md exception; this is the
  measurement it asks for), or accept that 16 times only the character loop.
  No test — design. Measured 2026-09-27.
- **46-BENCH-WALL-UNDER-2X** (LOW, design) — deferred, trade-off. A native
  control of `rotten/` (guide × window × base, `-O3 -march=native`) takes 7.7 s
  CPU a case on both recipes, 1.54× the 5 s budget. A 2× wall needs about
  1.3·10⁶ bases, where the Go sliding window of `hints/06.md` (3.6 s a case at
  10⁶) passes 4.7 s and stops fitting the budget; C's takes 2.3 s. The same
  triple loop with the window loop innermost (one pass per guide base, adding
  into a byte counter per window) does the same O(guides × genome × L)
  comparisons, vectorizes 32 windows at a time, and takes 1.0 s a case (golden
  0.9 s), so no genome length separates it from the golden; `make vec` was not
  run on it. **Fix:** owner's call — accept the 1.5× wall and the swapped-loop
  pass, or reshape the level. No test — design. Measured 2026-09-27.
- **41-RANGE-WALL-UNDER-2X** (LOW, design) — deferred, trade-off.
  `10_large_range` (3·10⁵ inserts, then 5·10⁴ narrow range counts) holds a
  native control of `rotten/` to 8.7 s CPU at `-O3 -march=native`, 1.74× the
  5 s budget, while the Python golden takes 3.1 s. The golden spends about
  10 µs on an insert and on a narrow range count, so no mix of the two that
  keeps it within a third of the 10 s Python timeout reached a 2× wall.
  **Fix (optional):** a faster golden. No test — design. Measured 2026-09-27.

## vec grader

- **VEC-WORK-BEFORE-SOLVE** (MED, grading) — Record-only, needs the owner's
  decision. `scripts/vec_check.py` traces only `solve`, so work the program
  does before `solve` is entered is not graded. The solver edits the code that
  runs then: C's `input_parse` lives in `solution.c`, a C
  `__attribute__((constructor))` or a Go `init` runs before `main`, and Rust's
  `src/main.rs` and Go's `main.go` sit beside the edited file. Any of them can
  compute the answer for `solve` to copy out, or start a thread or process
  that finishes it before `solve` starts; the grader stops other threads and
  refuses other processes only from `solve`'s entry. **Fix:** a contract change
  in CLAUDE.md: move `input_parse` out of `solution.c` into a harness file the
  solver does not edit, and have `lint()` refuse code that runs before `main`
  (constructors, `.init_array` sections, Go `init`) in the edited files.
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
