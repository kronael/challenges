# challenges/

Personal coding-practice bench. 30 self-contained challenges, one per sitting.
Harness is **editor + `make test`**. Each challenge has its own dir `NN-slug/`.

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

## Make targets (same in every language dir)

| target | does |
|--------|------|
| `fmt`   | format (ruff format / gofmt / cargo fmt) |
| `lint`  | ruff check / go vet / cargo clippy |
| `check` | `fmt` then `lint` |
| `test`  | runs `check` first, then the test suite |
| `bench` | builds the release binary, times it on large cases |

- `make test` → `check` (fmt+lint) runs first, then the suite
  (`pytest -v` / `go test -v ./...` / `cargo test`).
- `make bench` → builds the **release** binary once, runs it on every
  `cases/??_large_*.in`, prints `<ms>` per case or `TIMEOUT`.

## TIMEOUT

`make bench` enforces a per-case wall-clock limit. Defaults: **5s** (Rust/Go),
**10s** (Python). Override per run:

```bash
make bench TIMEOUT=30
```

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

- 01, 08–20: full cases + tests (ready to solve).
- 21–30: README + harness scaffolded, `cases/` still empty (need generating).
- 02–07: sys challenges, stress tests in place.

## Sources

CSES, CP-Algorithms, USACO Guide, Project Euler, Codeforces EDU, CLRS. Per-
challenge attribution and URLs are in the catalog and "Sources" section of
`README.md`.
