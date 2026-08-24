# Spec — Go solver layout: `solution.go` (solve) + `main.go` (IO)

Status: adopted 2026-08-23. Applies to every I/O challenge's `go/` directory and
`template/go/`.

## Motivation

`solve` should read as a clean function — the solver opens one file and sees the
problem, not JSON decoding, stdin wiring, and output formatting. This mirrors the
Rust `src/lib.rs` (solve) / `src/main.rs` (thin binary) split adopted in v0.1.3.

Go cannot put a `solve` "library" in a *separate package* in the same directory
(one directory = one package), so the equivalent is a **two-file, single
`package main`** split. It gives the same isolation and needs no build changes.

## Layout (I/O challenges)

- **`go/solution.go`** — `package main`. Contains ONLY `func solve(...)` (plus any
  *solution-only* helper funcs). This is the single file the solver edits; the
  body is a stub (`return nil` / zero value). No `encoding/json`, no `os`, no IO.
- **`go/main.go`** — `package main`. The IO scaffold, complete: imports, the JSON
  `input` type (and its `UnmarshalJSON` when the input is heterogeneous), any
  output-`format` helper, and `func main()` = decode stdin JSON → call `solve` →
  print the one-line answer.
- **`go/solution_test.go`** — `package main`, unchanged. Drives the tracked cases
  through `solve` directly (same package → no import needed).
- **`go.mod`, `Makefile`** — unchanged. The Makefile builds in package mode
  (`go build .`, `go vet ./...`, `gofmt -w .`), so it picks up `solution.go`
  automatically; no rule references a bare `main.go`.

## Rules

- `solution.go` carries no IO concerns. Anything about *parsing* input or
  *formatting* output (the JSON struct, `UnmarshalJSON`, a `format`/join helper)
  lives in `main.go`.
- `solve`'s signature is the Input contract, unchanged by the split, so the test
  file and callers are untouched.
- Keep both files `package main`. Do not introduce a `solution` subpackage — it is
  heavier than a one-sitting challenge warrants and buys nothing here.

## Exceptions (already clean — do not split)

- **API challenges 21, 22** — function-only, tested directly; keep their existing
  `solution.go` with no `main`.
- **sys Go challenges 29, 30, 32, 34** — concurrency solvers in `solution.go` /
  `barrier.go` with no stdin/stdout `main`; unchanged. (sys 31, 33 have no `go/`.)

## Migration (2026-08-23)

56 I/O `go/main.go` files plus `template/go/main.go` were split by an
AST-position splitter (find the `solve` FuncDecl, slice the original bytes so doc
comments/bodies survive, `go/format` both files). Stub `solve` bodies use no
imports, so the split is import-clean. Verified: all 57 dirs pass `go build .`
and `go vet ./...`. The 6 heterogeneous dirs (24, 26, 35, 41, 51 with
`UnmarshalJSON`; 54 with `format`) correctly keep those IO helpers in `main.go`.

## Verify

```
for d in [0-9][0-9]-*/go template/go; do (cd "$d" && go build -o /dev/null . && go vet ./...) || echo "FAIL $d"; done
```
