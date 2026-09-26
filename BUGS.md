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
  does not count general-purpose arithmetic or stack accesses inside an
  iteration that loads a vector, because that is where Go spills and where every
  language keeps its per-vector loop control, bounds checks, and mask
  arithmetic. A `solve` that loads a vector, stores it to a local array, and
  then handles each lane with scalar code unrolled inside that same iteration
  therefore grades vectorized. It takes deliberate construction; no natural
  shape of 66–68 does it, and every separate scalar pass, every scalar
  floating-point add, and every heap load or store still counts. **Fix
  (optional):** tell apart stack slots that hold spilled vectors, which needs
  data flow the tracer does not track.

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
- **VEC-LINT-TEXT-ONLY** (LOW, hardening) — Record-only. `lint()` in
  `scripts/vec_check.py` regex-scans the text of every file under the solver
  directory, so it cannot see what only the language resolves: a C keyword or
  attribute name built by token pasting or named by a macro
  (`#define T target` then `__attribute__((T("avx512f")))`), a trigraph or
  digraph `#pragma`, a file outside the directory that a C `#include`, a Rust
  `include!` or `#[path]`, a Cargo `[lib] path`, or a Go `replace` pulls in, and
  the code of a Cargo or Go dependency. The build itself is open too (not
  tried): a solver Makefile can override the `main` recipe that
  `shared/c/io.mk` defines, and a `.cargo/config.toml` can set
  `build.rustc-wrapper`. Each takes deliberate construction. **Fix:** grade the
  preprocessed C (`cc -E` with the build's flags, system headers dropped), and
  refuse include paths that leave the directory, recipe overrides, and cargo
  config files.
