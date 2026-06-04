# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# challenges/

Personal coding-practice bench. 40 self-contained challenges, one per sitting.
Harness is **editor + `make test`**. Each challenge has its own dir `NN-slug/`.

## Golden rule — solutions ONLY in golden/

**io challenges** have four language dirs: `golden/`, `python/`, `go/`, `rust/`.

- **`golden/main.py`** — the optimised reference. Always passes `make test`.
  Never shown to the solver. Used to generate `.out` files and as the bench target.
- **`python/main.py`, `go/main.go`, `rust/src/main.rs`** — stubs ONLY.
  `solve()` must contain only `pass` / `return nil` / `todo!()`.

**sys challenges** (02–07): Python is inappropriate (GIL prevents real concurrency).
Use **`golden/main.c`** as the reference implementation instead of `main.py`.
`golden/main.c` contains the complete algorithm + a pthreads stress test in one file.
`golden/Makefile` builds with `gcc -std=c11 -O2 -pthread` and `make test` runs `./main`.

**Never put a working solution in `python/`, `go/`, or `rust/`.** If you find one,
move it to `golden/` and replace the original with a stub.

When scaffolding a new challenge: write the reference first in `golden/main.py`,
verify it passes, then write stubs in the three solver dirs.

## Two challenge types

- **io** (01, 08–30): program reads JSON from stdin, writes the answer to
  stdout. Correctness is checked against files in `cases/`.
- **sys** (02–07): concurrent / lock-free systems challenge. No `cases/`, no
  stdin/stdout. The test *is* a stress test written in the language (many
  threads, barrier-synced, assert the invariant).

## Layout

```
NN-slug/
  README.md              problem statement, constraints, examples, source link
  cases/                 NN.in / NN.out          (io only)
  python/  solution.py · test_solution.py · Makefile
  go/      main.go · solution_test.go · go.mod · Makefile
  rust/    src/lib.rs · src/main.rs · tests/ · Cargo.toml · Makefile
```

sys challenges have no `python/`; rust-only sys challenges (04, 06) have no `go/`.

## Input / output format

- **Input is always JSON**, structured to match the problem
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
| `bench` | build, then time binary on every `??_large_*.in` |
| `help`  | print all targets |

Running `make` (no target) = fmt + build + lint + test.

`make bench` uses `timeout -k 2 $(TIMEOUT)` — SIGTERM then SIGKILL 2s later,
so the loop can **never hang** regardless of what the binary does.
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
are timed by `bench`; the `??_large_` glob is what selects them.

## Languages

- **py** — `uv run` (pytest, ruff); no venv to manage.
- **go** — stdlib `go test`.
- **rs** — `cargo test`. io: `src/main.rs` is the timed binary; sys: `src/bin/bench.rs`.

Per-challenge language set is in the README catalog (most are `py go rs`; some
hard io and the sys ones drop a language).

## Adding a challenge

1. Copy `template/` to `NN-slug/` (next number).
2. Fill `README.md`: statement, constraints, examples, source URL.
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

- 01, 08–20, 34–40: full cases + tests (ready to solve).
- 21–33: README + harness scaffolded, `cases/` still empty (need generating).
- 02–07: sys challenges, stress tests in place.

## Sources

CSES, CP-Algorithms, USACO Guide, Project Euler, Codeforces EDU, CLRS. Per-
challenge attribution and URLs are in the catalog and "Sources" section of
`README.md`.
