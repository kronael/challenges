# challenges/

A personal coding-practice bench: 30 self-contained algorithm and systems
challenges, one per sitting, each solvable in Python, Go, and Rust against a
shared `make test` harness. Built for daily practice, not for an audience.

---

## How it works

Each challenge is a self-contained directory:

```
NN-slug/
  README.md           ← problem statement, examples, source link
  cases/              ← *.in / *.out  (for I/O challenges)
  python/             ← solution.py · test_solution.py · Makefile
  go/                 ← main.go · *_test.go · go.mod · Makefile
  rust/               ← src/lib.rs · src/main.rs · tests/ · Cargo.toml · Makefile
```

**Two types:**
- **io** — program reads JSON from stdin, writes answer to stdout. Test cases are files.
- **sys** — concurrent/systems challenge; no stdin/stdout. Test is a stress test in the language.

**Input format:** JSON. Chosen so parsing is real work, not just `split()`.
Structured keys match the problem (e.g. `{"n": 4, "edges": [...], "loads": [...]}`).

**Output format:** space-separated values on one line (integers or floats).

**Testing:**
```bash
cd NN-slug/rust   && make test    # cargo test — runs all cases/ and stress tests
cd NN-slug/go     && make test    # go test -v ./...
cd NN-slug/python && make test    # uv run --with pytest pytest -v

cd NN-slug/rust   && make bench   # time binary on large inputs (cases/??_large_*.in)
```

Large cases (`??_large_*.in`) are generated alongside correctness cases. `make bench`
builds once and times the binary on them — a direct measure of solution speed.

---

## Adding a challenge

1. Copy `template/` to `NN-slug/` (next number in sequence).
2. Edit `NN-slug/README.md`: problem statement, constraints, examples, source URL.
3. Add `cases/01.in`, `cases/01.out`, … (at least 6 small + 2–3 large).
4. Implement `solve()` in each language stub (the test harness is already wired).
5. Add a line to the catalog table below.

**With Claude:** paste the problem statement and ask Claude to
(a) write the cases, (b) write a reference implementation in Python, (c) scaffold
the Go/Rust stubs. The harness is already there — Claude only needs to fill in `solve()`.

```
"Add challenge 31: <problem statement>. Generate 8 small cases + 2 large (n=100k),
write a Python reference, scaffold Go and Rust stubs in challenges/31-slug/."
```

---

## Catalog

| # | Name | Key concept | Diff | Source | Lang |
|---|------|------------|------|--------|------|
| [01](01-edge-costs/) | Vertex Load Assignment | graph BFS, max-propagation | med | original | py go rs |
| [02](02-mpsc-queue/) | Vyukov MPSC Queue | lock-free, broken-link window | hard | [1024cores.net](https://www.1024cores.net/home/lock-free-algorithms/queues/non-intrusive-mpsc-node-based-queue) | go rs |
| [03](03-seqlock/) | Seqlock | memory ordering, torn reads | hard | Boehm MSPC 2012 | go rs |
| [04](04-work-stealing-deque/) | Chase-Lev Deque | lock-free, seq_cst last element | expert | [Chase & Lev SPAA 2005](https://fzn.fr/readings/ppopp13.pdf) | rs |
| [05](05-spsc-ring-buffer/) | SPSC Ring Buffer | false sharing, shadow counter | hard | [LMAX Disruptor](https://lmax-exchange.github.io/disruptor/disruptor.html) | go rs |
| [06](06-hazard-pointer-stack/) | Hazard-Pointer Stack | ABA, guess-publish-verify | expert | [Maged Michael 2004](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf) | rs |
| [07](07-sense-barrier/) | Sense-Reversing Barrier | barrier reuse, fence ordering | hard | Herlihy & Shavit | go rs |
| [08](08-lis/) | Longest Increasing Subsequence | patience sort, binary search | med | CLRS §15.4 | py go rs |
| [09](09-edit-distance/) | Edit Distance | 2-D DP, Levenshtein | med | CLRS §15.5 | py go rs |
| [10](10-coin-change/) | Coin Change | unbounded knapsack DP | med | CLRS | py go rs |
| [11](11-interval-scheduling/) | Interval Scheduling | greedy + exchange argument | med | CLRS §16.1 | py go rs |
| [12](12-count-inversions/) | Count Inversions | merge-sort invariant | med | CLRS | py go rs |
| [13](13-dijkstra/) | Dijkstra + Negative-Edge Guard | priority-queue shortest path | med | CLRS §24.3 | py go rs |
| [14](14-union-find/) | Union-Find (DSU) | path compression + rank | med | CLRS §21 | py go rs |
| [15](15-binary-search-answer/) | Binary Search on Answer | predicate + monotone search | med | [CF EDU](https://codeforces.com/edu/courses) | py go rs |
| [16](16-sliding-window-max/) | Sliding Window Maximum | monotone deque | med | [LeetCode 239](https://leetcode.com/problems/sliding-window-maximum/) | py go rs |
| [17](17-max-subarray/) | Maximum Subarray (Kadane) | DP, online algorithm | easy | CLRS §4.1 | py go rs |
| [18](18-prime-sieve/) | Sieve of Eratosthenes | prime generation + counting | med | [PE #10](https://projecteuler.net/problem=10) | py go rs |
| [19](19-mod-exp/) | Fast Modular Exponentiation | repeated squaring | easy | CLRS §31.6 | py go rs |
| [20](20-matrix-exp/) | Matrix Exponentiation | Fibonacci in O(log n) | med | competitive classic | py go rs |
| [21](21-kmp/) | KMP + Z-function | failure function, linear match | med | [CSES #2107](https://cses.fi/problemset/task/2107) | py go rs |
| [22](22-segment-tree/) | Segment Tree Range Sum | lazy propagation | hard | [CSES EDU](https://cses.fi/problemset/) | py go rs |
| [23](23-knapsack/) | Knapsack 0/1 | bounded DP | med | CLRS | py go rs |
| [24](24-toposort/) | Topological Sort | DFS finish time, cycle detect | med | CLRS §22.4 | py go rs |
| [25](25-mst/) | Minimum Spanning Tree | Kruskal + DSU | med | CLRS §23 | py go rs |
| [26](26-matrix-chain/) | Matrix Chain Multiplication | interval DP, optimal parens | hard | CLRS §15.2 | py go rs |
| [27](27-lcs/) | Longest Common Subsequence | 2-D DP, reconstruction | med | CLRS §15.4 | py go rs |
| [28](28-prime-pair-sets/) | Prime Pair Sets | Miller-Rabin + clique search | hard | [PE #60](https://projecteuler.net/problem=60) | py go rs |
| [29](29-distinct-substrings/) | Distinct Substrings | suffix array + LCP | hard | [CSES #2105](https://cses.fi/problemset/task/2105) | py go rs |
| [30](30-max-flow/) | Max Flow / Min Cut | Dinic's algorithm | hard | [CSES #1694](https://cses.fi/problemset/task/1694) | py go rs |
| [31](31-go-memory-model/) | Go Memory Model Quizzes | happens-before, atomics, false sharing | hard | go.dev/ref/mem | go |
| [32](32-prolog-thinking/) | Relational Programming | logic/CSP, run predicates backward | med | Prolog / python-constraint | py |
| [33](33-haskell-thinking/) | Lazy Eval & Corecursion | infinite generators, pipelines | med | Haskell / itertools | py |
| [34](34-trie-autocomplete/) | Trie + Autocomplete | trie, DFS, lexicographic order | med | [LeetCode 1268](https://leetcode.com/problems/search-suggestions-system/) | py go rs |
| [35](35-lru-cache/) | LRU Cache | doubly-linked list + hashmap, O(1) | med | [LeetCode 146](https://leetcode.com/problems/lru-cache/) | py go rs |
| [36](36-running-median/) | Running Median | two heaps, balance invariant | med | [LeetCode 295](https://leetcode.com/problems/find-median-from-data-stream/) | py go rs |
| [37](37-fenwick-tree/) | Fenwick Tree (BIT) | prefix sums, bit trick i&(-i) | med | [CP-Algorithms](https://cp-algorithms.com/data_structures/fenwick.html) | py go rs |
| [38](38-skip-list/) | Skip List | probabilistic linked list, O(log n) | hard | [Pugh 1990](https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf) | py go rs |
| [39](39-rope/) | Rope (String Builder) | binary tree of fragments, O(log n) concat | hard | [Boehm et al. 1995](https://www.cs.rit.edu/usr/local/pub/jeh/courses/QUARTERS/FP/Labs/CedarRope/rope-paper.pdf) | py go rs |

**Ready (cases or stress tests in place):** 01–20, 31–33  
**Scaffolded (README + harness, cases empty):** 21–30  
**Building now:** 34–39 (data structures)

---

## Up next

Candidate problems with a source picked out, but **no directory yet** — not
scaffolded, no harness, no cases. Pulled from the backlog when starting a new one.

| Name | Key concept | Source |
|------|------------|--------|
| Bipartite Matching | max-flow reduction, König's theorem | [CSES #1696](https://cses.fi/problemset/task/1696) |
| Goldbach's Other Conjecture | counterexample search, primality | [PE #46](https://projecteuler.net/problem=46) |
| Coin Partitions | pentagonal number theorem | [PE #78](https://projecteuler.net/problem=78) |
| Poker Hands | comparator design, no edge cases | [PE #54](https://projecteuler.net/problem=54) |
| Path Sum Grid | grid DP → Dijkstra on grid | [PE #81–83](https://projecteuler.net/problem=81) |
| Counting Paths on Tree | Euler tour + Fenwick + LCA | [CSES #1136](https://cses.fi/problemset/task/1136) |
| Aho-Corasick | multi-pattern match, trie automaton | [CSES #2102](https://cses.fi/problemset/task/2102) |
| Watching Cowflix | tree DP + parametric search | [USACO Feb 2023 Plat](https://usaco.org/index.php?page=viewproblem2&cpid=1310) |

---

## Design decisions

**JSON input.** Parsing a JSON edge-list is real work; parsing three ints on a
line is not. It forces a clean `Input` struct in every language.

**`test` vs `bench`.** Correctness runs fast (< 5s) and gates on fmt+lint.
`bench` runs only the large inputs and prints wall-clock times — you read the
number and decide if it's fast enough.

**Native tooling only.** `uv run pytest`, `go test`, `cargo test` — each
language's own runner handles discovery, parallelism, and output. No wrappers,
no shared runner.

**`cases/` as plain files.** Trivial to add, diff, and generate. A database
would add ceremony for no benefit.

---

## Sources

Where the problems and reference algorithms come from.

| Source | What's there |
|--------|-------------|
| [CSES Problem Set](https://cses.fi/problemset/) | 300 problems, all categories, clean I/O |
| [CP-Algorithms](https://cp-algorithms.com) | reference proofs + implementations |
| [USACO Guide](https://usaco.guide) | Bronze→Platinum, best graph/DP explanations |
| [USACO Contests](https://usaco.org/index.php?page=contests) | the original platinum-division problems |
| [Project Euler](https://projecteuler.net) | math-heavy; problems 1–100 are one afternoon each |
| [Codeforces EDU](https://codeforces.com/edu/courses) | structured tracks: segment tree, strings, flows |
| [LeetCode](https://leetcode.com/problemset/) | clean single-concept drills |
| [CLRS](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) | *Introduction to Algorithms* — the textbook home of the classics |
