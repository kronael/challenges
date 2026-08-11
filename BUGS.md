# Defect log

## Status — 2026-08-11 — Challenge 35 benchmark review

- **CH35-LARGE-PREFIX-ESCAPE** (HIGH, bench) — Both large fixtures use only
  full-array sums at `35-hard-dynamic-range-sums/cases/09_large_mixed.in:1` and
  `35-hard-dynamic-range-sums/cases/10_large_queries.in:1`; the second has no
  updates, and a correct native prefix array with linear suffix repair passes
  both under the five-second limit. **Fix:** Give both fixtures varied wide
  ranges and enough interleaved low-index updates to make native rescan and
  linear-update controls independently time out with margin.
- **CH35-ROTTEN-DOC-OVERCLAIM** (LOW, docs) — `HINTS.md:23` says the rotten
  reference demonstrates both documented linear strategies, but
  `rotten/main.py:5` implements only range rescanning. **Fix:** State that the
  executable rotten reference demonstrates rescanning and native controls
  validate both strategies.

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
