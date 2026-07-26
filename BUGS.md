Audit 2026-07-26 (codex adversarial sweep, each finding reproduced against the
code before recording). Record-only per the Bug Triage Protocol — none fixed.

## C1 — 48 shortest-superstring golden is wrong and crashes on valid input (2026-07-26, open)

Neither reference performs the README-required duplicate/contained-read
reduction. For `{"reads":["TTA","GATTACA"]}` the answer is `GATTACA` (TTA is a
substring) but golden prints `TTA` and rotten prints `TTAGATTACA`.
`{"reads":["AAAA","AAAA"]}` crashes golden with `StopIteration`. A golden that is
wrong — or aborts — on valid input breaks the whole contract.

- **Severity:** high
- **Scope:** challenge 48 references
- **Affected:** `48-hard-shortest-superstring/golden/main.py`, `.../rotten/main.py`
- **Source:** `48-hard-shortest-superstring/golden/main.py:43`
- **Status:** open
- **Fix:**

## C2 — 41 ordered-set golden range_count is O(n) per query, times out at spec max (2026-07-26, open)

The skip list has the structure for sub-linear rank queries, but `range_count`
walks node-by-node from `lo` to `hi`, so a full-range query is O(n) and the whole
run is O(n²). 50k inserts + 50k full-range counts — within the documented 10⁵-op
cap — exceeds the 10s golden budget (reproduced: exit 124). The fast reference is
not fast.

- **Severity:** high
- **Scope:** challenge 41 golden
- **Affected:** `41-hard-ordered-set-queries/golden/main.py`
- **Source:** `41-hard-ordered-set-queries/golden/main.py:74`
- **Status:** open
- **Fix:**

## C3 — 07 coin-change golden/rotten don't dedup denominations; README bounds none (2026-07-26, open)

The references loop over every denomination for every amount, and the README
bounds `amount` (`≤ 2,000,000`) but not the coin-list length or uniqueness.
`{"amount":50000,"coins":[1]*10000}` is valid and should return `50000`, but
golden exceeds its 10s budget (reproduced: exit 124). Either the golden must dedup
denominations or the README must bound/​distinct the coin list.

- **Severity:** medium
- **Scope:** challenge 07 references + spec
- **Affected:** `07-medium-coin-change/golden/main.py`, `.../rotten/main.py`, `.../README.md`
- **Source:** `07-medium-coin-change/golden/main.py:8`
- **Status:** open
- **Fix:**

## C4 — 45 k-mer rotten is wrong on a small valid input (2026-07-26, open)

Rotten assumes the first listed fragment identifies the reconstruction start, so
it is not correct even on small inputs. `{"k":2,"kmers":["AC","GA","AG"]}` has the
unique result `AGAC` (golden agrees), but rotten prints `AC`. A rotten control must
be correct on every valid small input and fail only on the large ones.

- **Severity:** medium
- **Scope:** challenge 45 rotten
- **Affected:** `45-hard-kmer-assembly/rotten/main.py`
- **Source:** `45-hard-kmer-assembly/rotten/main.py:20`
- **Status:** open
- **Fix:**

## C5 — 31 work-stealing deque capacity is half the documented size (2026-07-26, open)

The C golden and the c/ scaffold allocate `1<<21` (2,097,152) slots, but the
README promises a fixed capacity of 4,194,304 (`1<<22`). A valid state with more
than 2,097,152 queued tasks cannot be represented; the stresses use only 1,000,000
/ 500,000 tasks so they never expose it. (Pre-existing in golden/main.c; the same
constant was copied into the new c/ scaffold.)

- **Severity:** medium
- **Scope:** challenge 31 golden + C scaffold
- **Affected:** `31-hard-work-stealing-deque/golden/main.c:15`, `.../c/solution.h:9`
- **Source:** `31-hard-work-stealing-deque/README.md:22`
- **Status:** open
- **Fix:**

## C6 — Out-of-domain large fixtures in 43 and 48 (2026-07-26, open)

`43/cases/09_large_deep_book.in` has 220,000 orders but the README caps orders at
`2·10⁵`. `48/cases/10_large_chain.in` and `11_large_dense.in` each have 20,001
reads but the README caps reads at 20,000. A conforming solver that sizes to the
documented maximum can fail `bench` on inputs it was never required to accept, and
the 48 fixtures no longer prove the rotten timeout inside the stated domain.

- **Severity:** medium
- **Scope:** fixtures vs spec
- **Affected:** `43-hard-order-book/cases/09_large_deep_book.in`, `48-hard-shortest-superstring/cases/{10_large_chain,11_large_dense}.in`
- **Source:** `43-hard-order-book/README.md:41`, `48-hard-shortest-superstring/README.md:24`
- **Status:** open
- **Fix:**

## C7 — 30 tick-snapshot stress miscounts the initial all-zero snapshot as torn (2026-07-26, open)

`consistent_value()` returns 0 both when the eight slots disagree (genuinely
torn) and when they all legitimately hold 0. The writer starts at counter 1, so a
reader that reads the initial state (seq 0, all zeros) after the barrier but before
the first publication gets value 0 and increments `torn`, failing a correct
implementation. Value 0 is overloaded as both "torn" and "genuine zero snapshot".

- **Severity:** medium
- **Scope:** challenge 30 C stress harness
- **Affected:** `30-hard-consistent-tick-snapshot/c/stress.c`
- **Source:** `30-hard-consistent-tick-snapshot/c/stress.c:62`
- **Status:** open
- **Fix:**

## C8 — Shared C io harness trims trailing whitespace, contradicting the byte-exact contract (2026-07-26, open)

`template/c/test.c` (byte-identical across all 48 io c/ dirs) strips trailing
spaces, tabs, CRs, and newlines from both actual and expected before comparing, so
`42\n` and `42 \t\r\n\n` compare equal. `make bench` compares byte-for-byte
(`cmp -s`), so a solution with trailing whitespace passes `test` but fails `bench`
— the two disagree on what "correct output" means.

- **Severity:** medium
- **Scope:** shared C io test harness (all 48)
- **Affected:** `template/c/test.c` and every `NN-*/c/test.c`
- **Source:** `template/c/test.c:24`, `template/c/test.c:84`
- **Status:** open
- **Fix:**

## C9 — 53–57 test harnesses reintroduce the T1/T3 false-green class (2026-07-26, open)

The 9e500ba fix (BUGS T1/T3) never covered 53–57, added later. Their Go suites
(all five) and Rust mains lack the `assert !ins.is_empty()` nonempty-case guard
that earlier challenges have, and the Go suites ignore the `.out` read error and
(53,55,56,57) the integer-parse error (`out, _ := os.ReadFile`; `want, _ :=
strconv.Atoi`). Python 54–57 lack `assert CASES`. An absent/empty cases dir, or a
missing `.out` matched by a zero-valued wrong solve, is reported as passing.

- **Severity:** medium
- **Scope:** 53–57 Go / Rust / Python case harnesses
- **Affected:** `{53..57}/go/solution_test.go`, `{53..57}/rust/src/main.rs`, `{54..57}/python/test_solution.py`
- **Source:** `53-hard-circular-genome-distance/go/solution_test.go:26`
- **Status:** open
- **Fix:**

## CA — root sys-rotten target accepts any nonzero exit as "controlled failure" (2026-07-26, open)

`make sys-rotten` treats every nonzero status except timeout (124) as successful
exposure of the intended defect. A compile error, segfault, or unrelated assertion
(status 2) is reported as a passing controlled failure, so a rotten control that is
simply broken — rather than exposing its documented hazard — still passes the
contract check.

- **Severity:** low
- **Scope:** root contract harness
- **Affected:** `Makefile` (`sys-rotten` target)
- **Source:** `Makefile:93`
- **Status:** open
- **Fix:**

## CB — Weak test invariants let degenerate solutions pass (2026-07-26, open)

Several suites assert too little: 21 (Python + Go) checks coloring count and
per-coloring validity but not distinctness, so returning N copies of one coloring
passes while omitting the rest; 22 (Python + Go) tests `sieve` only on the same
stream `primes` uses, so a `sieve` that ignores its argument passes; the 29 and 33
C stress tests check per-value multiplicity / alloc-free totals but not exact-once
identity, so a lost-and-duplicated pair with equal counts passes. Also 21/22 README
bodies still say to implement `main.py` only, though a Go track now exists.

- **Severity:** low
- **Scope:** test-strength across 21, 22, 29, 33
- **Affected:** `21-*/python/test_solution.py:51`, `21-*/go/solution_test.go:101`, `22-*/{python,go}` sieve tests, `29-*/c/stress.c`, `33-*/c/stress.c`, `21-*/README.md`, `22-*/README.md`
- **Source:** `22-medium-unbounded-sequences/python/test_solution.py:25`
- **Status:** open
- **Fix:**

## CC — 30 seqlock golden copies a non-atomic payload (C11 data race) (2026-07-26, open)

`golden/main.c` (and the c/ scaffold type) `memcpy` a plain non-atomic `data`
buffer inside the seqlock while a reader may `memcpy` it concurrently — a C11 data
race that the sequence counter does not legalize under the abstract machine. This
is the textbook seqlock and works on real hardware, so likely a documented
tradeoff rather than a fix; recorded for completeness.

- **Severity:** low
- **Scope:** challenge 30 golden + C scaffold (inherent to the pattern)
- **Affected:** `30-hard-consistent-tick-snapshot/golden/main.c:19`, `.../c/solution.h:10`
- **Source:** `30-hard-consistent-tick-snapshot/golden/main.c:19`
- **Status:** open
- **Fix:**
