# Coding Challenges

52 self-contained algorithm and systems challenges. Most use file-based cases,
an optimized reference, a deliberately naive benchmark control, and stubs in
Python, Go, and Rust. A few exercises use an API test suite or a systems stress
test instead. Run `make` in a language directory to format, build, lint, and test.

---

## Quick start

```bash
# pick a challenge, pick a language
cd 05-medium-price-streak/rust && make       # fmt → build → lint → test
cd 05-medium-price-streak/go   && make bench # check and time your solution on large inputs
```

From the repo root, verify the whole bench at once:

```bash
make test    # every golden + rotten passes its case suite
make golden  # every golden passes test AND bench (stays fast)
make rotten  # verify every rotten reference behaves as expected
make sys     # the sys (29-34) C stress tests pass
make sys-rotten # sys controls pass sanity and fail controlled stress
```

Every language directory has the same five targets:

| target  | does |
|---------|------|
| `make`  | fmt → build → lint → test (default) |
| `make test`  | correctness — small cases only, fast |
| `make bench` | correctness + speed — compare every large result, then report time |
| `make fmt`   | format in place |
| `make help`  | list all targets |

---

## Structure

```
NN-level-slug/
  README.md      ← the problem only: task, constraints, I/O, examples
  HINTS.md       ← the approach/technique — spoilers, open only when stuck
  cases/         ← NN.in / NN.out  (I/O challenges)
  golden/        ← optimized reference; always passes make test
  rotten/        ← deliberately naive benchmark control
  python/        ← stub: implement solve() in main.py
  go/            ← stub: implement solve() in main.go
  rust/          ← stub: implement solve() in src/main.rs
```

The `README.md`, challenge title, directory slug, and catalog never narrow the
solution search. All guidance, including rejected approaches and complexity
comparisons, lives in `HINTS.md`.

**Two challenge types:**

- **io** — reads JSON from stdin, writes space-separated values to stdout
- **api** — implements functions checked directly by a language test suite
- **sys** — exposes a systems API; the test is a stress test rather than files

I/O challenge input is always JSON
(`{"n":4,"edges":[[0,1]],"loads":[10,null]}`), so parsing is real work rather
than splitting whitespace.

---

## Challenges

Difficulty is based on prerequisite depth, correctness edge cases,
implementation burden, and the constraints enforced by `make bench`.

| # | Name | Level | Lang |
|---|------|-------|------|
| [01](01-easy-max-subarray/) | Maximum Subarray | easy | py go rs |
| [02](02-easy-mod-exp/) | Modular Power | easy | py go rs |
| [03](03-easy-max-drawdown/) | Max Drawdown | easy | py go rs |
| [04](04-medium-edge-costs/) | Vertex Load Assignment | medium | py go rs |
| [05](05-medium-price-streak/) | Price Streak | medium | py go rs |
| [06](06-medium-edit-distance/) | Edit Distance | medium | py go rs |
| [07](07-medium-coin-change/) | Coin Change | medium | py go rs |
| [08](08-medium-interval-scheduling/) | Interval Scheduling | medium | py go rs |
| [09](09-medium-count-inversions/) | Count Inversions | medium | py go rs |
| [10](10-medium-route-costs/) | Route Costs | medium | py go rs |
| [11](11-medium-friend-groups/) | Friend Groups | medium | py go rs |
| [12](12-medium-textbook-split/) | Textbook Split | medium | py go rs |
| [13](13-medium-sliding-window-max/) | Sliding Window Maximum | medium | py go rs |
| [14](14-medium-count-primes/) | Count Primes | medium | py go rs |
| [15](15-medium-huge-fibonacci/) | Huge Fibonacci | medium | py go rs |
| [16](16-medium-string-search/) | String Search | medium | py go rs |
| [17](17-medium-knapsack/) | 0/1 Knapsack | medium | py go rs |
| [18](18-medium-task-ordering/) | Task Ordering | medium | py go rs |
| [19](19-medium-mst/) | Cheapest Road Network | medium | py go rs |
| [20](20-medium-lcs/) | Longest Common Subsequence | medium | py go rs |
| [21](21-medium-constraint-puzzles/) | Constraint Puzzles | medium | py |
| [22](22-medium-unbounded-sequences/) | Unbounded Sequences | medium | py |
| [23](23-medium-search-suggestions/) | Search Suggestions | medium | py go rs |
| [24](24-medium-lru-cache/) | Cache Eviction | medium | py go rs |
| [25](25-medium-running-median/) | Running Median | medium | py go rs |
| [26](26-medium-dynamic-prefix-sums/) | Dynamic Prefix Sums | medium | py go rs |
| [27](27-medium-weighted-job-scheduling/) | Weighted Job Scheduling | medium | py go rs |
| [28](28-medium-news-feed-merge/) | News Feed Merge | medium | py go rs |
| [29](29-hard-mpsc-queue/) | Multi-Producer Queue | hard | go rs |
| [30](30-hard-consistent-tick-snapshot/) | Consistent Tick Snapshot | hard | go rs |
| [31](31-hard-work-stealing-deque/) | Concurrent Owner/Thief Deque | hard | rs |
| [32](32-hard-two-thread-buffer/) | Two-Thread Buffer | hard | go rs |
| [33](33-hard-lock-free-stack-reclamation/) | Lock-Free Stack Reclamation | hard | rs |
| [34](34-hard-reusable-spin-barrier/) | Reusable Spin Barrier | hard | go rs |
| [35](35-hard-dynamic-range-sums/) | Dynamic Range Sums | hard | py go rs |
| [36](36-hard-matrix-chain/) | Matrix Chain Multiplication | hard | py go rs |
| [37](37-hard-prime-pair-sets/) | Prime Pair Sets | hard | py go rs |
| [38](38-hard-distinct-substrings/) | Distinct Substrings | hard | py go rs |
| [39](39-hard-max-flow/) | Max Flow | hard | py go rs |
| [40](40-hard-go-memory-model/) | Go Concurrency Quizzes | hard | go |
| [41](41-hard-ordered-set-queries/) | Ordered Set Queries | hard | py go rs |
| [42](42-hard-fragmented-string-queries/) | Fragmented String Queries | hard | py go rs |
| [43](43-hard-order-book/) | Order Book | hard | py go rs |
| [44](44-hard-affine-align/) | Affine Alignment Score | hard | py go rs |
| [45](45-hard-kmer-assembly/) | K-mer Assembly | hard | py go rs |
| [46](46-hard-crispr-offtarget/) | CRISPR Off-Targets | hard | py go rs |
| [47](47-hard-rna-max-pairs/) | RNA Max Pairs | hard | py go rs |
| [48](48-hard-shortest-superstring/) | Shortest Superstring | hard | py go rs |
| [49](49-hard-gene-region-decoder/) | Gene Region Decoder | hard | py go rs |
| [50](50-hard-tree-sequence-likelihood/) | Tree Sequence Likelihood | hard | py go rs |
| [51](51-hard-deadline-scheduler/) | Deadline Scheduler | hard | py go rs |
| [52](52-hard-service-pairing/) | Service Pairing | hard | py go rs |

---

## Adding a challenge

Copy `template/`, fill in `README.md`, add `cases/`, implement `solve()`.
The harness is already wired — `make` will work immediately.

---

## Sources

Each challenge keeps solution-neutral attribution in its `README.md`.
Solution-bearing references live in `HINTS.md`.

---

## License

Public domain — [Unlicense](UNLICENSE).
