# Coding Challenges

48 self-contained algorithm and systems challenges. Each has a problem statement,
test cases, a golden reference solution, and stubs to implement in Python, Go,
and Rust. Run `make` in any language directory to format, build, lint, and test.

---

## Quick start

```bash
# pick a challenge, pick a language
cd 08-price-streak/rust && make       # fmt → build → lint → test
cd 08-price-streak/go   && make bench # check and time your solution on large inputs
```

From the repo root, verify the whole bench at once:

```bash
make test    # every golden + rotten passes its case suite
make golden  # every golden passes test AND bench (stays fast)
make rotten  # verify every rotten reference behaves as expected
make sys     # the sys (02-07) C stress tests pass
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
NN-slug/
  README.md      ← the problem only: task, constraints, I/O, examples
  HINTS.md       ← the approach/technique — spoilers, open only when stuck
  cases/         ← NN.in / NN.out  (small correctness + large bench)
  golden/        ← optimised reference; always passes make test
  rotten/        ← benchmark-control reference
  python/        ← stub: implement solve() in main.py
  go/            ← stub: implement solve() in main.go
  rust/          ← stub: implement solve() in src/main.rs
```

The `README.md`, challenge title, directory slug, and catalog never narrow the
solution search. All guidance, including rejected approaches and complexity
comparisons, lives in `HINTS.md`.

**Two challenge types:**
- **io** — reads JSON from stdin, writes space-separated values to stdout
- **sys** — concurrent/systems challenge; the test is a stress test, not files

**Input is always JSON** (`{"n":4,"edges":[[0,1]],"loads":[10,null]}`) so
parsing is real work rather than splitting whitespace.

---

## Challenges

| # | Name | Diff | Lang |
|---|------|------|------|
| [01](01-edge-costs/) | Vertex Load Assignment | med | py go rs |
| [02](02-mpsc-queue/) | Multi-Producer Queue | hard | go rs |
| [03](03-consistent-tick-snapshot/) | Consistent Tick Snapshot | hard | go rs |
| [04](04-work-stealing-deque/) | Concurrent Owner/Thief Deque | expert | rs |
| [05](05-two-thread-buffer/) | Two-Thread Buffer | hard | go rs |
| [06](06-lock-free-stack-reclamation/) | Lock-Free Stack Reclamation | expert | rs |
| [07](07-reusable-spin-barrier/) | Reusable Spin Barrier | hard | go rs |
| [08](08-price-streak/) | Price Streak | med | py go rs |
| [09](09-edit-distance/) | Edit Distance | med | py go rs |
| [10](10-coin-change/) | Coin Change | med | py go rs |
| [11](11-interval-scheduling/) | Interval Scheduling | med | py go rs |
| [12](12-count-inversions/) | Count Inversions | med | py go rs |
| [13](13-route-costs/) | Route Costs | med | py go rs |
| [14](14-friend-groups/) | Friend Groups | med | py go rs |
| [15](15-textbook-split/) | Textbook Split | med | py go rs |
| [16](16-sliding-window-max/) | Sliding Window Maximum | med | py go rs |
| [17](17-max-subarray/) | Maximum Subarray | easy | py go rs |
| [18](18-count-primes/) | Count Primes | med | py go rs |
| [19](19-mod-exp/) | Modular Power | easy | py go rs |
| [20](20-huge-fibonacci/) | Huge Fibonacci | med | py go rs |
| [21](21-string-search/) | String Search | med | py go rs |
| [22](22-dynamic-range-sums/) | Dynamic Range Sums | hard | py go rs |
| [23](23-knapsack/) | 0/1 Knapsack | med | py go rs |
| [24](24-task-ordering/) | Task Ordering | med | py go rs |
| [25](25-mst/) | Cheapest Road Network | med | py go rs |
| [26](26-matrix-chain/) | Matrix Chain Multiplication | hard | py go rs |
| [27](27-lcs/) | Longest Common Subsequence | med | py go rs |
| [28](28-prime-pair-sets/) | Prime Pair Sets | hard | py go rs |
| [29](29-distinct-substrings/) | Distinct Substrings | hard | py go rs |
| [30](30-max-flow/) | Maximum Network Flow | hard | py go rs |
| [31](31-go-memory-model/) | Go Concurrency Quizzes | hard | go |
| [32](32-constraint-puzzles/) | Constraint Puzzles | med | py |
| [33](33-unbounded-sequences/) | Unbounded Sequences | med | py |
| [34](34-search-suggestions/) | Search Suggestions | med | py go rs |
| [35](35-lru-cache/) | Cache Eviction | med | py go rs |
| [36](36-running-median/) | Running Median | med | py go rs |
| [37](37-dynamic-prefix-sums/) | Dynamic Prefix Sums | med | py go rs |
| [38](38-ordered-set-queries/) | Ordered Set Queries | hard | py rs |
| [39](39-fragmented-string-queries/) | Fragmented String Queries | hard | py rs |
| [40](40-weighted-job-scheduling/) | Weighted Job Scheduling | med | py go rs |
| [41](41-order-book/) | Order Book | hard | py go rs |
| [42](42-news-feed-merge/) | News Feed Merge | med | py go rs |
| [43](43-max-drawdown/) | Max Drawdown | easy | py go rs |
| [44](44-affine-align/) | Affine Alignment Score | hard | py go rs |
| [45](45-kmer-assembly/) | K-mer Assembly | hard | py go rs |
| [46](46-crispr-offtarget/) | CRISPR Off-Targets | hard | py go rs |
| [47](47-rna-max-pairs/) | RNA Max Pairs | hard | py go rs |
| [48](48-shortest-superstring/) | Shortest Superstring | hard | py go rs |

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
