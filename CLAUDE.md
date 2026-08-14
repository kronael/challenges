# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Never commit build artifacts

NEVER stage compiled output. ALWAYS gitignore it, give its Makefile a `clean`
target, and run exhaustive root `make clean` before every commit. This includes
C `main`/`run_tests`/`stress`/`benchmark`, Go binaries, and Rust `target/`.

## Teaching mode — no free solutions

When helping the user solve a challenge in this repo, act as a teacher, not
an answer key. NEVER reveal the solution approach, the named algorithm, or
even a hint from `HINTS.md` unless the user has explicitly asked for a hint
or the solution **twice** (two separate, explicit requests — not implied by
frustration or a vague "I'm stuck"). Before that threshold: ask guiding
questions, point at relevant concepts to review, or explain why an approach
fails — never state the technique or write solving code for them.

# challenges/

Personal coding-practice bench. 57 self-contained challenges, one per sitting.
Harness is **editor + `make test`**. Each challenge has its own dir
`NN-level-slug/`.

## Golden rule — solutions ONLY in golden/

**io challenges** have five language dirs: `golden/`, `python/`, `go/`, `rust/`, `c/`.

- **`golden/main.py`** — the optimised reference. Always passes `make test`.
  Never shown to the solver. Used to generate tracked small `.out` files and
  ephemeral expected benchmark output.
- **`rotten/`** — its OWN dir, a sibling of `golden/` (same shape: `main.py` +
  `Makefile` + `pyproject.toml`, never a file nested inside `golden/`). It holds
  the *naive* reference: correct, so `make test` PASSES the small cases, but too
  slow, so `make bench` TIMEOUTs. It is the trap the solver must beat — the
  obvious O(n²)/exponential approach the problem punishes. `rotten/`'s test
  runs only tracked small cases. (sys
  challenges: `rotten/main.c` is the obvious-but-wrong version — torn reads, false
  sharing, ABA — that passes a weak check but fails the stress test / race
  detector.)
  Every rotten implementation must be short, obviously correct on small inputs,
  and deliberately naive. Put a concise code-level comment next to the naive
  operation that states what is recomputed or enumerated, its complexity, and why
  the large cases time out. Never add sleeps, busy-work, input-name checks, wrong
  answers, or other artificial benchmark sabotage.
  For io challenges this is an executable contract: `make test` must finish
  promptly and match every tracked fixture, and every generated large case must
  independently exercise the documented naive bottleneck at the default timeout.
  Validate that wall with an equivalent temporary native control compiled with
  optimization and the fastest supported solver timeout; a Python-only timeout
  is insufficient evidence. Keep the temporary control outside the repository so
  it cannot expose a solution or be mistaken for a solver scaffold.
  A small fixture must never duplicate a generated large case byte-for-byte. Rotten code
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
- **`python/main.py`, `go/main.go`, `rust/src/lib.rs`, `c/solution.c`** — stubs
  ONLY. Only the algorithm body is a stub (`pass` / `return nil` / `todo!()` /
  a zero `Answer`); the scaffold around it must be COMPLETE — `solve(...)`
  signature matches the Input, `main` parses JSON → calls `solve` → prints, and
  the test harness actually runs the cases through `solve`. A finished stub
  builds and its tests run (and fail only on the unimplemented body), never on
  harness/parse errors.
  Rust keeps a plain derived `Input` beside `solve`. Heterogeneous JSON decoding
  lives in `src/input.rs`, with its solver-facing types re-exported by `lib.rs`;
  never pass `serde_json::Value` into `solve`.
  The I/O C runner, fixture driver, JSON reader, allocation helpers, and build
  rules live once in `shared/c/`. Every I/O challenge's `c/Makefile` includes
  `../../shared/c/io.mk`. Per challenge, write only `solution.h` (the `Input`
  and `Answer` types plus the five prototypes) and `solution.c` (`input_parse`,
  `input_free`, `answer_print`, `answer_free` complete; `solve` stubbed).
  `input_parse` transcribes the JSON literally — a precomputed adjacency list,
  sort, or prefix sum in there is a solution hint and belongs in `golden/`.

**sys challenges** (29–34): Python is inappropriate (GIL prevents real concurrency).
Use **`golden/main.c`** as the reference implementation instead of `main.py`.
`golden/main.c` contains the complete algorithm + a pthreads stress test in one file.
`golden/Makefile` builds with `gcc -std=c11 -O2 -pthread` and `make test` runs `./main`.
Their `c/` solver dir keeps `solution.h` + `solution.c` (types and lifecycle
complete, every concurrent operation stubbed to `abort()`), plus a finished
`stress.c` and `bench.c`.

**Never put a working solution in `python/`, `go/`, `rust/`, or `c/`.** If you find
one, move it to `golden/` and replace the original with a stub.

When scaffolding a new I/O challenge: write the reference first in
`golden/main.py`, verify it passes, then write stubs in the four solver dirs.

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
shared/c/               shared I/O C runner, JSON reader, tests, and Make rules
scripts/large_cases.py  deterministic seeded benchmark recipes
scripts/bench.py        ephemeral generation, oracle comparison, and timeout runner
NN-level-slug/
  README.md              problem statement, constraints, I/O, examples
  HINTS.md               all solution guidance and solution-bearing sources
  cases/                 tracked small NN.in / NN.out fixtures (io only)
  golden/  main.py · test_solution.py · Makefile · pyproject.toml   (fast reference)
  rotten/  main.py · test_solution.py · Makefile · pyproject.toml   (naive trap: passes test, fails bench)
  python/  main.py · test_solution.py · Makefile
  go/      main.go · solution_test.go · go.mod · Makefile
  rust/    src/lib.rs · src/main.rs · tests/ · Cargo.toml · Makefile
  c/       solution.h · solution.c · Makefile (includes shared/c/io.mk)
```

sys challenges have no `python/`; sys challenges 31 and 33 have no `go/`.
API challenges 21 and 22 have only `python/` and `go/`.

## Input / output format

- **I/O challenge input is always JSON**, structured to match the problem
  (`{"n": 4, "edges": [...], "loads": [...]}`). Deliberate: forces real
  parsing into an `Input` struct, not `line.split()`.
- **Output is exactly one line** in the format documented by the challenge
  `README.md`.

## Make targets

I/O solver directories share these targets:

| target  | does |
|---------|------|
| `all`   | **default** — runs fmt → build → lint → test in sequence |
| `build` | compile / syntax-check (`cargo build` / `go build .` / `python -c "import main"`) |
| `fmt`   | format in place (ruff / gofmt / cargo fmt) |
| `lint`  | static analysis (ruff check / go vet / cargo clippy) |
| `check` | fmt then lint |
| `test`  | build + check + tracked small-case suite |
| `bench` | generate seeded large cases, check output, then report elapsed time |
| `help`  | print all targets |

Running `make` (no target) = fmt + build + lint + test.

For I/O solvers, `make bench` generates one input at a time under `tmp/`, runs
the golden implementation to obtain the expected output, and compares solver
stdout byte-for-byte. The input, expected output, and actual output are deleted
before the next seed. Configured repeat runs share one aggregate time budget. A
timeout, runtime error, or mismatch fails the target.
The runner terminates the whole process group, then kills it 2s later, so the
benchmark can **never hang** regardless of what the binary does.
Defaults: **5s** Rust/Go, **10s** Python. Override: `make bench TIMEOUT=30`.

I/O `golden/` has `all: test` and adds a `regen` target to regenerate tracked
small `.out` files. API, sys, and quiz challenges use targets specific to their test style;
check their README and `make help` instead of assuming this table applies.

## Test case coverage

Every I/O challenge must have at least eight challenge-appropriate small cases.
Cover valid boundary or degenerate inputs, representative ordinary inputs, a
no-op or already-valid input where meaningful, adversarial inputs for common
mistakes, and the largest useful input that still belongs in the small suite.
For graph inputs, include at least two relevant shapes such as a path, star,
cycle, or dense graph.

Every I/O challenge must also have at least two structurally distinct seeded
large-case recipes. Each one must independently exercise the documented rotten
bottleneck at the default timeout.

When writing cases, include valid inputs that expose likely implementation
mistakes. Edge cases are the point — don't just use the README examples.

## Large cases

Define each recipe in `scripts/large_cases.py` with a `??_large_NAME` name, such
as `09_large_path`. Seeds are derived from the challenge number and recipe
ordinal. `make cases` regenerates every case hash and rejects any drift from the
frozen aggregate digest, including seed and repeat metadata. `make bench`
materializes these cases ephemerally.

## Languages

- **py** — `uv run` (pytest, ruff); no venv to manage.
- **go** — stdlib `go test`.
- **rs** — `cargo test`. io: `src/main.rs` is the timed binary; sys: `src/bin/bench.rs`.
- **c** — `cc -std=c11`, no dependencies. io: `./run_tests` drives `../cases`,
  `./main` is the timed binary; sys: `./stress` and `./benchmark`. `lint`
  recompiles everything with `-Wpedantic -Wshadow -Werror`.

Per-challenge language set is in the README catalog (most are `py go rs`; some
hard io and the sys ones drop a language).

## Adding an I/O challenge

1. Copy `template/` to `NN-level-slug/` (next number).
2. Fill `README.md`: statement, constraints, I/O, and examples. Put all solution
   guidance and solution-bearing sources in `HINTS.md`.
3. Add at least eight tracked small fixture pairs and at least two seeded recipes
   in `scripts/large_cases.py`, update the frozen digest, then run `make cases`.
4. Implement only `golden/` and `rotten/`. Tailor each solver scaffold to the
   input contract, but keep its `solve()` body stubbed. For `c/`, keep the
   one-line Makefile include from `template/c/` and write only `solution.h` and
   `solution.c`; do not copy files from `shared/c/`.
5. Verify the golden test and bench pass, the rotten small test passes, and every
   generated case exceeds both the rotten timeout and the fastest solver timeout when
   exercised by an equivalent optimized temporary native control.
6. Add a row to the catalog table in the repo `README.md`.

For an API, sys, or quiz challenge, copy the closest matching challenge instead
of the I/O template and preserve that challenge type's test contract.

## No debug prints

Do not add print/println/fmt.Println debug output to solutions. The io test
harness compares stdout exactly — any extra line breaks the test. More
importantly: if you need a print to understand what the code does, you don't
have a mental model of it yet. Build the model first, write the code second.
The race detector and the stress test are your debugger for sys challenges.

## State of the repo

- 01–20, 23–28, 35–39, 41–57: io challenges with cases and language harnesses.
- 21–22: Python API exercises with direct tests and no rotten reference.
- 29–34: sys challenges with stress tests.
- 40: standalone Go concurrency quizzes.

## Sources

CSES, CP-Algorithms, USACO Guide, Project Euler, Codeforces EDU, CLRS,
peer-reviewed papers, and official technical documentation. Keep
solution-neutral attribution in the challenge README. Put solution-bearing
attribution in `HINTS.md`.

# Project Memory

- Rotten references should be the shortest obviously correct naive formulation,
  with an adjacent complexity/timeout comment. Every generated large case must exercise
  that bottleneck independently in optimized native code as well as Python;
  systems controls pair a passing weak sanity test with a deterministic
  adversarial failure.
