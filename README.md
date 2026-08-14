# Coding Challenges

57 self-contained algorithm and systems challenges. Most use file-based cases,
an optimized reference, a deliberately naive benchmark control, and stubs in
Python, Go, Rust, and C. A few exercises use an API test suite or a systems
stress test instead. Run `make` in a language directory to format, build, lint,
and test.

---

## Quick start

```bash
# pick a challenge, pick a language
make -C 05-medium-price-streak/rust       # fmt → build → lint → test
make -C 05-medium-price-streak/go bench   # check and time your solution on large inputs
```

From the repo root, verify the whole bench at once:

```bash
make test        # I/O and API golden suites; I/O rotten small suites pass
make cases       # all seeded large-case recipes reproduce their frozen hashes
make golden      # I/O and API golden tests pass; I/O benchmarks stay fast
make rotten      # I/O rotten controls pass small cases; every large case times out
make sys         # systems golden C stress tests pass
make sys-rotten  # systems controls pass sanity and fail controlled stress
```

I/O solver directories share these targets:

| target  | does |
|---------|------|
| `make`  | fmt → build → lint → test (default) |
| `make build` | compile or syntax-check |
| `make fmt`   | format in place |
| `make lint`  | run static analysis |
| `make check` | format, then lint |
| `make test`  | correctness — small cases only, fast |
| `make bench` | correctness + speed — generate and check every seeded large case |
| `make help`  | list all targets |

API, systems, and quiz challenges use targets suited to their test style. Their
challenge README and `make help` list the available commands.

---

## I/O challenge structure

```
NN-level-slug/
  README.md      ← the problem only: task, constraints, I/O, examples
  HINTS.md       ← the approach/technique — spoilers, open only when stuck
  cases/         ← tracked small NN.in / NN.out fixtures (I/O challenges)
  golden/        ← optimized reference; always passes make test
  rotten/        ← deliberately naive benchmark control
  python/        ← stub: implement solve() in main.py
  go/            ← stub: implement solve() in main.go
  rust/          ← stub: implement solve() in src/lib.rs
  c/             ← stub: implement solve() in solution.c
```

The reusable C scaffold lives once in `shared/c/`: JSON parsing, allocation
helpers, the executable entry point, the fixture runner, and their Make rules.
Each challenge's `c/` directory contains only `solution.c`, `solution.h`, and a
one-line Makefile include. `input_parse` and `answer_print` are written for you;
`solve()` is not.

Large benchmark inputs are deterministic recipes in `scripts/large_cases.py`,
not checked-in payloads. `make bench` materializes one seeded case at a time in
`tmp/`, asks the golden implementation for its expected output, checks the
solver under one aggregate budget (including configured repeat runs), and
deletes all three temporary files. Frozen hashes and recipe metadata make drift
fail `make cases`.

The `README.md`, challenge title, directory slug, and catalog never narrow the
solution search. All guidance, including rejected approaches and complexity
comparisons, lives in `HINTS.md`.

**Four challenge types:**

- **io** — reads JSON from stdin and writes one line in the documented format
- **api** — implements functions checked directly by a language test suite
- **sys** — exposes a systems API; the test is a stress test rather than files
- **quiz** — asks for predictions about standalone programs, then checks them

I/O challenge input is always JSON
(`{"n":4,"edges":[[0,1]],"loads":[10,null]}`), so parsing is real work rather
than splitting whitespace.

---

## Challenges

Difficulty is based on prerequisite depth, correctness edge cases,
implementation burden, and the constraints enforced by `make bench`.

| # | Name | Level | Lang |
|---|------|-------|------|
| [01](01-easy-max-subarray/) | Maximum Subarray | easy | py go rs c |
| [02](02-easy-mod-exp/) | Modular Power | easy | py go rs c |
| [03](03-easy-max-drawdown/) | Max Drawdown | easy | py go rs c |
| [04](04-medium-edge-costs/) | Vertex Load Assignment | medium | py go rs c |
| [05](05-medium-price-streak/) | Price Streak | medium | py go rs c |
| [06](06-medium-edit-distance/) | Edit Distance | medium | py go rs c |
| [07](07-medium-coin-change/) | Coin Change | medium | py go rs c |
| [08](08-medium-interval-scheduling/) | Interval Scheduling | medium | py go rs c |
| [09](09-medium-count-inversions/) | Count Inversions | medium | py go rs c |
| [10](10-medium-route-costs/) | Route Costs | medium | py go rs c |
| [11](11-medium-friend-groups/) | Friend Groups | medium | py go rs c |
| [12](12-medium-textbook-split/) | Textbook Split | medium | py go rs c |
| [13](13-medium-sliding-window-max/) | Sliding Window Maximum | medium | py go rs c |
| [14](14-medium-count-primes/) | Count Primes | medium | py go rs c |
| [15](15-medium-huge-fibonacci/) | Huge Fibonacci | medium | py go rs c |
| [16](16-medium-string-search/) | String Search | medium | py go rs c |
| [17](17-medium-knapsack/) | 0/1 Knapsack | medium | py go rs c |
| [18](18-medium-task-ordering/) | Task Ordering | medium | py go rs c |
| [19](19-medium-mst/) | Cheapest Road Network | medium | py go rs c |
| [20](20-medium-lcs/) | Longest Common Subsequence | medium | py go rs c |
| [21](21-medium-constraint-puzzles/) | Constraint Puzzles | medium | py go |
| [22](22-medium-unbounded-sequences/) | Unbounded Sequences | medium | py go |
| [23](23-medium-search-suggestions/) | Search Suggestions | medium | py go rs c |
| [24](24-medium-lru-cache/) | Cache Eviction | medium | py go rs c |
| [25](25-medium-running-median/) | Running Median | medium | py go rs c |
| [26](26-medium-dynamic-prefix-sums/) | Dynamic Prefix Sums | medium | py go rs c |
| [27](27-medium-weighted-job-scheduling/) | Weighted Job Scheduling | medium | py go rs c |
| [28](28-medium-news-feed-merge/) | News Feed Merge | medium | py go rs c |
| [29](29-hard-mpsc-queue/) | Multi-Producer Queue | hard | go rs c |
| [30](30-hard-consistent-tick-snapshot/) | Consistent Tick Snapshot | hard | go rs c |
| [31](31-hard-work-stealing-deque/) | Concurrent Owner/Thief Deque | hard | rs c |
| [32](32-hard-two-thread-buffer/) | Two-Thread Buffer | hard | go rs c |
| [33](33-hard-lock-free-stack-reclamation/) | Lock-Free Stack Reclamation | hard | rs c |
| [34](34-hard-reusable-spin-barrier/) | Reusable Spin Barrier | hard | go rs c |
| [35](35-hard-dynamic-range-sums/) | Dynamic Range Sums | hard | py go rs c |
| [36](36-hard-matrix-chain/) | Matrix Chain Multiplication | hard | py go rs c |
| [37](37-hard-prime-pair-sets/) | Prime Pair Sets | hard | py go rs c |
| [38](38-hard-distinct-substrings/) | Distinct Substrings | hard | py go rs c |
| [39](39-hard-max-flow/) | Max Flow | hard | py go rs c |
| [40](40-hard-go-memory-model/) | Go Concurrency Quizzes | hard | go |
| [41](41-hard-ordered-set-queries/) | Ordered Set Queries | hard | py go rs c |
| [42](42-hard-fragmented-string-queries/) | Fragmented String Queries | hard | py go rs c |
| [43](43-hard-order-book/) | Order Book | hard | py go rs c |
| [44](44-hard-affine-align/) | Affine Alignment Score | hard | py go rs c |
| [45](45-hard-kmer-assembly/) | K-mer Assembly | hard | py go rs c |
| [46](46-hard-crispr-offtarget/) | CRISPR Off-Targets | hard | py go rs c |
| [47](47-hard-rna-max-pairs/) | RNA Max Pairs | hard | py go rs c |
| [48](48-hard-shortest-superstring/) | Shortest Superstring | hard | py go rs c |
| [49](49-hard-gene-region-decoder/) | Gene Region Decoder | hard | py go rs c |
| [50](50-hard-tree-sequence-likelihood/) | Tree Sequence Likelihood | hard | py go rs c |
| [51](51-hard-deadline-scheduler/) | Deadline Scheduler | hard | py go rs c |
| [52](52-hard-service-pairing/) | Service Pairing | hard | py go rs c |
| [53](53-hard-circular-genome-distance/) | Circular Genome Distance | hard | py go rs c |
| [54](54-hard-spectrum-peptide-recovery/) | Spectrum Peptide Recovery | hard | py go rs c |
| [55](55-hard-changing-network-queries/) | Changing Network Queries | hard | py go rs c |
| [56](56-hard-orthogonal-segment-crossings/) | Orthogonal Segment Crossings | hard | py go rs c |
| [57](57-hard-causal-event-replay/) | Causal Event Replay | hard | py go rs c |

---

## Adding a challenge

1. Copy `template/` to the next numbered directory.
2. Write the pure specification in `README.md`. Put all solution guidance and
   solution-bearing sources in `HINTS.md`.
3. Add the optimized implementation in `golden/` and the short, correct, naive
   control in `rotten/`. Keep every solver `solve` body stubbed.
4. Add at least eight tracked small fixture pairs and at least two structurally
   distinct seeded recipes to `scripts/large_cases.py`. Update the frozen digest
   after an intentional recipe change, then verify it with `make cases`; each
   generated input must independently make the rotten implementation exceed its
   timeout.
5. Run the root `make golden` and `make rotten` contract checks.
6. Add the challenge to the catalog above.

---

## Sources

Each challenge keeps solution-neutral attribution in its `README.md`.
Solution-bearing references live in `HINTS.md`. Upstream problem sets and
reference works are credited in [NOTICE](NOTICE).

Development assisted by Claude Code (Anthropic).

---

## License

GNU General Public License v3.0 — [LICENSE](LICENSE).
