# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Teaching mode — no free solutions

When helping the user solve a challenge in this repo, act as a teacher, not
an answer key. NEVER reveal the solution approach, the named algorithm, or
even a hint from `HINTS.md` unless the user has explicitly asked for a hint
or the solution **twice** (two separate, explicit requests — not implied by
frustration or a vague "I'm stuck"). Before that threshold: ask guiding
questions, point at relevant concepts to review, or explain why an approach
fails — never state the technique or write solving code for them.

# challenges/

Personal coding-practice bench. 52 self-contained challenges, one per sitting.
Harness is **editor + `make test`**. Each challenge has its own dir
`NN-level-slug/`.

## Golden rule — solutions ONLY in golden/

**io challenges** have four language dirs: `golden/`, `python/`, `go/`, `rust/`.

- **`golden/main.py`** — the optimised reference. Always passes `make test`.
  Never shown to the solver. Used to generate `.out` files and as the bench target.
- **`rotten/`** — its OWN dir, a sibling of `golden/` (same shape: `main.py` +
  `Makefile` + `pyproject.toml`, never a file nested inside `golden/`). It holds
  the *naive* reference: correct, so `make test` PASSES the small cases, but too
  slow, so `make bench` TIMEOUTs. It is the trap the solver must beat — the
  obvious O(n²)/exponential approach the problem punishes. `rotten/`'s test
  excludes the `_large_` cases (those are exactly where it would hang). (sys
  challenges: `rotten/main.c` is the obvious-but-wrong version — torn reads, false
  sharing, ABA — that passes a weak check but fails the stress test / race
  detector.)
  Every rotten implementation must be short, obviously correct on small inputs,
  and deliberately naive. Put a concise code-level comment next to the naive
  operation that states what is recomputed or enumerated, its complexity, and why
  the large cases time out. Never add sleeps, busy-work, input-name checks, wrong
  answers, or other artificial benchmark sabotage.
  For io challenges this is an executable contract: `make test` must finish
  promptly and match every non-`_large_` fixture, and every `??_large_*.in` must
  independently exercise the documented naive bottleneck at the default timeout.
  A small fixture must never duplicate a large fixture byte-for-byte. Rotten code
  must remain correct for every input allowed by `README.md`, not only the checked
  fixtures. Keep it as the shortest direct formulation; do not retain memoization,
  compatibility caches, branch-and-bound pruning, fast precomputation, or other
  optimizations that obscure the intended complexity wall.
  For sys challenges, separate a weak sanity target that passes from an adversarial
  `stress`, `race`, or `bench` target that reliably exposes the documented failure.
  Do not depend on architecture luck, an unbounded hang, or an implementation
  spin cutoff. Prefer barrier-controlled interleavings. Performance traps require
  pinned, warmed-up, repeated measurements and an asserted regression.
  The root `make sys-rotten` target enforces the sanity-pass/adversarial-fail
  contract and rejects hangs.
- **`python/main.py`, `go/main.go`, `rust/src/main.rs`** — stubs ONLY.
  Only the algorithm body is a stub (`pass` / `return nil` / `todo!()`); the
  scaffold around it must be COMPLETE — `solve(...)` signature matches the Input,
  `main` parses JSON → calls `solve` → prints, and the test harness actually runs
  the cases through `solve`. A finished stub builds and its tests run (and fail
  only on the unimplemented body), never on harness/parse errors.

**sys challenges** (29–34): Python is inappropriate (GIL prevents real concurrency).
Use **`golden/main.c`** as the reference implementation instead of `main.py`.
`golden/main.c` contains the complete algorithm + a pthreads stress test in one file.
`golden/Makefile` builds with `gcc -std=c11 -O2 -pthread` and `make test` runs `./main`.

**Never put a working solution in `python/`, `go/`, or `rust/`.** If you find one,
move it to `golden/` and replace the original with a stub.

When scaffolding a new challenge: write the reference first in `golden/main.py`,
verify it passes, then write stubs in the three solver dirs.

## README vs HINTS — never spoil the problem

- **`README.md`** is a pure specification: task, constraints, I/O format, worked
  examples, and a source only when the citation itself reveals nothing about the
  solution. It must not name, describe, compare, or rule out any solution method.
  This ban includes techniques, data structures, memory orderings, recurrences,
  invariants, implementation shapes, failed strategies, naive or brute-force
  approaches, complexity analysis of candidate approaches, and phrases such as
  "the trick", "the trap", "the catch", or "the hard part". State the input
  limits without explaining how an approach behaves at those limits.
- **Names are part of the prompt.** Challenge titles, directory slugs, catalog
  rows, example captions, and source labels must also be solution-neutral.
- **`HINTS.md`** holds every detail that could narrow the solution search: the
  approach, named algorithm, data structure, ordering, old "Teaches" bullets,
  rejected approaches, complexity comparisons, and solution-bearing sources.
  The solver opens it only when stuck.

## Challenge types

- **io**: program reads JSON from stdin, writes the answer to stdout.
  Correctness is checked against files in `cases/`.
- **api** (21–22): Python functions checked directly by a test suite. These do
  not use file fixtures or a `rotten/` benchmark control.
- **sys** (29–34): concurrent / lock-free systems challenge. No `cases/`, no
  stdin/stdout. The test *is* a stress test written in the language (many
  threads, barrier-synced, assert the invariant).
- **quiz** (40): standalone Go memory-model exercises. This does not use the
  golden/rotten layout.

## Layout

```
NN-level-slug/
  README.md              problem statement, constraints, I/O, examples
  HINTS.md               all solution guidance and solution-bearing sources
  cases/                 NN.in / NN.out          (io only)
  golden/  main.py · test_solution.py · Makefile · pyproject.toml   (fast reference)
  rotten/  main.py · test_solution.py · Makefile · pyproject.toml   (naive trap: passes test, fails bench)
  python/  main.py · test_solution.py · Makefile
  go/      main.go · solution_test.go · go.mod · Makefile
  rust/    src/lib.rs · src/main.rs · tests/ · Cargo.toml · Makefile
```

sys challenges have no `python/`; rust-only sys challenges (04, 06) have no `go/`.

## Input / output format

- **I/O challenge input is always JSON**, structured to match the problem
  (`{"n": 4, "edges": [...], "loads": [...]}`). Deliberate: forces real
  parsing into an `Input` struct, not `line.split()`.
- **Output is space-separated values on one line** (ints or floats).

## Make targets (identical in every language dir)

| target  | does |
|---------|------|
| `all`   | **default** — runs fmt → build → lint → test in sequence |
| `build` | compile / syntax-check (`cargo build` / `go build .` / `python -c "import main"`) |
| `fmt`   | format in place (ruff / gofmt / cargo fmt) |
| `lint`  | static analysis (ruff check / go vet / cargo clippy) |
| `check` | fmt then lint |
| `test`  | build + check + test suite — **small cases only** (no `_large_`) |
| `bench` | build, check output for every `??_large_*.in`, then report elapsed time |
| `help`  | print all targets |

Running `make` (no target) = fmt + build + lint + test.

`make bench` captures stdout and compares it byte-for-byte with the matching
`.out`. A timeout, missing expected output, runtime error, or mismatch fails the
target.
It uses `timeout -k 2 $(TIMEOUT)` — SIGTERM then SIGKILL 2s later, so the loop
can **never hang** regardless of what the binary does.
Defaults: **5s** Rust/Go, **10s** Python. Override: `make bench TIMEOUT=30`.

`golden/` has `all: test` and adds a `regen` target to regenerate `.out` files.

## Test case coverage

**Every challenge must cover these categories in its 8 small cases:**
- Minimal / degenerate input (n=0 or n=1 where valid)
- All-null / all-set inputs
- Single fixed value, all others propagate from it
- Two fixed values that meet in the middle
- Cycle / star / path — at least two graph shapes
- Values that propagate to the zero floor
- An already-correct input (no changes needed)
- Maximum constraint stress at small scale (n=8, densest graph)

**Large cases (`09_large_*`, `10_large_*`):**
- One that punishes O(n²): e.g. long path, 200k nodes
- One with different structure: star, caterpillar, or dense graph

When writing cases: if you can construct a valid input the naive algorithm
gets wrong or slow, include it. Edge cases are the point — don't just use
the README examples.

## Large cases

Named `??_large_NAME.in` / `.out` (e.g. `09_large_increasing.in`). Only these
are checked and timed by `bench`; the `??_large_` glob is what selects them.

## Languages

- **py** — `uv run` (pytest, ruff); no venv to manage.
- **go** — stdlib `go test`.
- **rs** — `cargo test`. io: `src/main.rs` is the timed binary; sys: `src/bin/bench.rs`.

Per-challenge language set is in the README catalog (most are `py go rs`; some
hard io and the sys ones drop a language).

## Adding a challenge

1. Copy `template/` to `NN-level-slug/` (next number).
2. Fill `README.md`: statement, constraints, I/O, and examples. Put a source URL
   in `HINTS.md` if its title or target reveals the solution.
3. io: add `cases/01.in`/`.out` … (≥6 small + 2–3 large); sys: write the stress
   test instead.
4. Implement `solve()` in each language stub — the harness is already wired.
5. Add a row to the catalog table in the repo `README.md`.

## No debug prints

Do not add print/println/fmt.Println debug output to solutions. The io test
harness compares stdout exactly — any extra line breaks the test. More
importantly: if you need a print to understand what the code does, you don't
have a mental model of it yet. Build the model first, write the code second.
The race detector and the stress test are your debugger for sys challenges.

## State of the repo

- 01–20, 23–28, 35–39, 41–52: io challenges with cases and language harnesses.
- 21–22: Python API exercises with direct tests and no rotten reference.
- 29–34: sys challenges with stress tests.
- 40: standalone Go concurrency quizzes.

## Sources

CSES, CP-Algorithms, USACO Guide, Project Euler, Codeforces EDU, CLRS,
peer-reviewed papers, and official technical documentation. Keep
solution-neutral attribution in the challenge README. Put solution-bearing
attribution in `HINTS.md`.
