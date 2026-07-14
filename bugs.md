## T1 — ✅ FIXED 2026-07-14 Python case harnesses pass when no cases are collected (2026-07-14, fixed)

Eighty-two case-driven Python test modules parametrize directly from a filesystem glob without asserting that the resulting case list is nonempty. If the case directory is missing, empty, or resolved from the wrong working directory, pytest reports skipped empty parameter sets and the suite can exit successfully without checking any expected output. The Python template reproduces the same unsafe default.

- **Severity:** medium
- **Scope:** Python solver and reference case harnesses
- **Affected:** solver harnesses for 01, 08–13, 15–19, 26–29, 34, 37–44, and 48 (26 files); both `golden/` and `rotten/` harnesses for 01, 08–12, 15–19, 21, 26–29, 34–35, 37–44, and 47–48 (28 files each); `template/python/test_solution.py`
- **Source:** `08-price-streak/python/test_solution.py:5`, `08-price-streak/golden/test_solution.py:8`, `08-price-streak/rotten/test_solution.py:9`, `template/python/test_solution.py:6`
- **Status:** resolved-not-yet-removed
- **Fix:** 9e500ba

## T2 — ✅ FIXED 2026-07-14 Reference tests ignore failed subprocess exit status (2026-07-14, fixed)

Forty-seven golden/rotten test modules compare captured stdout but never assert the subprocess return code. A reference executable can therefore print the expected text and then fail without failing the test; more concretely, the affected challenges 21, 22, 34, 37, 39, and 42 have legitimate whitespace-only expected outputs, so an input-specific crash that emits no stdout is accepted as correct for those cases.

- **Severity:** medium
- **Scope:** Python golden and rotten subprocess harnesses
- **Affected:** `golden/` for 08, 10–11, 15–17, 19, 21–22, 24, 26–30, 34, 37–40, and 42–44 (23 files); `rotten/` for the same challenges plus 01 (24 files)
- **Source:** `21-string-search/golden/test_solution.py:13`, `21-string-search/rotten/test_solution.py:14`, `21-string-search/cases/06.out`
- **Status:** resolved-not-yet-removed
- **Fix:** 9e500ba

## T3 — ✅ FIXED 2026-07-14 Dynamic range Go tests fabricate expectations after I/O errors (2026-07-14, fixed)

The Go harness for challenge 37 is the only case-driven Go suite that neither fails on an empty case list nor checks input/output and integer-parse errors. Missing expected output becomes an empty slice, invalid integers become zero, and malformed input is decoded as a zero-value struct, allowing damaged or absent fixtures to be mistaken for valid expected results.

- **Severity:** medium
- **Scope:** Go correctness harness
- **Affected:** `37-dynamic-prefix-sums/go/solution_test.go`
- **Source:** `37-dynamic-prefix-sums/go/solution_test.go:14`, `37-dynamic-prefix-sums/go/solution_test.go:24`, `37-dynamic-prefix-sums/go/solution_test.go:29`, `37-dynamic-prefix-sums/go/solution_test.go:32`
- **Status:** resolved-not-yet-removed
- **Fix:** 9e500ba
