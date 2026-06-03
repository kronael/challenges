# Coding Challenges

39 self-contained algorithm and systems challenges. Each has a problem statement,
test cases, a golden reference solution, and stubs to implement in Python, Go,
and Rust. Run `make` in any language directory to format, build, lint, and test.

---

## Quick start

```bash
# pick a challenge, pick a language
cd 08-lis/rust && make       # fmt → build → lint → test
cd 08-lis/go   && make bench # time your solution on large inputs
```

Every language directory has the same five targets:

| target  | does |
|---------|------|
| `make`  | fmt → build → lint → test (default) |
| `make test`  | correctness — small cases only, fast |
| `make bench` | speed — large inputs, 5s timeout per case |
| `make fmt`   | format in place |
| `make help`  | list all targets |

---

## Structure

```
NN-slug/
  README.md      ← problem, difficulty, what it teaches, source
  cases/         ← NN.in / NN.out  (small correctness + large bench)
  golden/        ← optimised Python reference; always passes make test
  python/        ← stub: implement solve() in main.py
  go/            ← stub: implement solve() in main.go
  rust/          ← stub: implement solve() in src/main.rs
```

**Two challenge types:**
- **io** — reads JSON from stdin, writes space-separated values to stdout
- **sys** — concurrent/systems challenge; the test is a stress test, not files

**Input is always JSON** (`{"n":4,"edges":[[0,1]],"loads":[10,null]}`) so
parsing is real work rather than splitting whitespace.

---

## Challenges

| # | Name | Key concept | Diff | Source | Lang |
|---|------|------------|------|--------|------|
| [01](01-edge-costs/) | Vertex Load Assignment | multi-source max-propagation | med | original | py go rs |
| [02](02-mpsc-queue/) | Vyukov MPSC Queue | lock-free, broken-link window | hard | [1024cores.net](https://www.1024cores.net/home/lock-free-algorithms/queues/non-intrusive-mpsc-node-based-queue) | go rs |
| [03](03-seqlock/) | Seqlock | memory ordering, torn reads | hard | [Boehm MSPC 2012](https://dl.acm.org/doi/10.1145/2247684.2247688) | go rs |
| [04](04-work-stealing-deque/) | Chase-Lev Work-Stealing Deque | lock-free, seq_cst last element | expert | [Chase & Lev SPAA 2005](https://fzn.fr/readings/ppopp13.pdf) | rs |
| [05](05-spsc-ring-buffer/) | SPSC Ring Buffer | false sharing, shadow counter | hard | [LMAX Disruptor](https://lmax-exchange.github.io/disruptor/disruptor.html) | go rs |
| [06](06-hazard-pointer-stack/) | Hazard-Pointer Stack | ABA, guess-publish-verify | expert | [Maged Michael 2004](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf) | rs |
| [07](07-sense-barrier/) | Sense-Reversing Barrier | barrier reuse, fence ordering | hard | [Herlihy & Shavit](https://dl.acm.org/doi/10.1145/62527.62529) | go rs |
| [08](08-lis/) | Longest Increasing Subsequence | patience sort, binary search | med | CLRS §15.4 | py go rs |
| [09](09-edit-distance/) | Edit Distance | 2-D DP, Levenshtein | med | CLRS §15.5 | py go rs |
| [10](10-coin-change/) | Coin Change | unbounded knapsack DP | med | CLRS | py go rs |
| [11](11-interval-scheduling/) | Interval Scheduling | greedy + exchange argument | med | CLRS §16.1 | py go rs |
| [12](12-count-inversions/) | Count Inversions | merge-sort invariant | med | CLRS | py go rs |
| [13](13-dijkstra/) | Dijkstra's Algorithm | priority-queue shortest path | med | CLRS §24.3 | py go rs |
| [14](14-union-find/) | Union-Find (DSU) | path compression + rank | med | CLRS §21 | py go rs |
| [15](15-binary-search-answer/) | Binary Search on Answer | predicate + monotone search | med | [CF EDU](https://codeforces.com/edu/courses) | py go rs |
| [16](16-sliding-window-max/) | Sliding Window Maximum | monotone deque | med | [LeetCode 239](https://leetcode.com/problems/sliding-window-maximum/) | py go rs |
| [17](17-max-subarray/) | Maximum Subarray (Kadane) | DP, online algorithm | easy | CLRS §4.1 | py go rs |
| [18](18-prime-sieve/) | Sieve of Eratosthenes | prime generation, segmented sieve | med | [PE #10](https://projecteuler.net/problem=10) | py go rs |
| [19](19-mod-exp/) | Fast Modular Exponentiation | repeated squaring | easy | CLRS §31.6 | py go rs |
| [20](20-matrix-exp/) | Matrix Exponentiation | linear recurrence in O(log n) | med | competitive classic | py go rs |
| [21](21-kmp/) | KMP + Z-function | failure function, Z-array | med | [CSES #2107](https://cses.fi/problemset/task/2107) | py go rs |
| [22](22-segment-tree/) | Segment Tree | range queries, point updates | hard | [CSES EDU](https://cses.fi/problemset/) | py go rs |
| [23](23-knapsack/) | Knapsack 0/1 | bounded DP | med | CLRS | py go rs |
| [24](24-toposort/) | Topological Sort | Kahn's BFS, cycle detection | med | CLRS §22.4 | py go rs |
| [25](25-mst/) | Minimum Spanning Tree | Kruskal + DSU | med | CLRS §23 | py go rs |
| [26](26-matrix-chain/) | Matrix Chain Multiplication | interval DP | hard | CLRS §15.2 | py go rs |
| [27](27-lcs/) | Longest Common Subsequence | 2-D DP | med | CLRS §15.4 | py go rs |
| [28](28-prime-pair-sets/) | Prime Pair Sets | Miller-Rabin + clique search | hard | [PE #60](https://projecteuler.net/problem=60) | py go rs |
| [29](29-distinct-substrings/) | Distinct Substrings | suffix array + LCP | hard | [CSES #2105](https://cses.fi/problemset/task/2105) | py go rs |
| [30](30-max-flow/) | Max Flow / Min Cut | Dinic's algorithm | hard | [CSES #1694](https://cses.fi/problemset/task/1694) | py go rs |
| [31](31-go-memory-model/) | Go Memory Model Quizzes | happens-before, atomics | hard | [go.dev/ref/mem](https://go.dev/ref/mem) | go |
| [32](32-prolog-thinking/) | Relational Programming | CSP, predicates run backward | med | python-constraint | py |
| [33](33-haskell-thinking/) | Lazy Evaluation & Corecursion | infinite generators, pipelines | med | itertools | py |
| [34](34-trie-autocomplete/) | Trie + Autocomplete | DFS, lexicographic suggestions | med | [LeetCode 1268](https://leetcode.com/problems/search-suggestions-system/) | py go rs |
| [35](35-lru-cache/) | LRU Cache | doubly-linked list + hashmap | med | [LeetCode 146](https://leetcode.com/problems/lru-cache/) | py go rs |
| [36](36-running-median/) | Running Median | two-heap balance invariant | med | [LeetCode 295](https://leetcode.com/problems/find-median-from-data-stream/) | py go rs |
| [37](37-fenwick-tree/) | Fenwick Tree (BIT) | prefix sums, i&(-i) trick | med | [CP-Algorithms](https://cp-algorithms.com/data_structures/fenwick.html) | py go rs |
| [38](38-skip-list/) | Skip List | probabilistic linked list | hard | [Pugh CACM 1990](https://dl.acm.org/doi/10.1145/78973.78977) | py rs |
| [39](39-rope/) | Rope | binary tree of string fragments | hard | [Boehm et al. 1995](https://dl.acm.org/doi/10.1145/214438.214444) | py rs |
| [40](40-weighted-job-scheduling/) | Weighted Job Scheduling | DP + binary search, O(n log n) | med | [CLRS §16.3](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) · [LC 1235](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | py go rs |

---

## Adding a challenge

Copy `template/`, fill in `README.md`, add `cases/`, implement `solve()`.
The harness is already wired — `make` will work immediately.

---

## Sources

| Source | What's there |
|--------|-------------|
| [CSES Problem Set](https://cses.fi/problemset/) | 300 problems, clean I/O, all categories |
| [Project Euler](https://projecteuler.net) | math-heavy; 1–100 are one afternoon each |
| [USACO Contests](https://usaco.org/index.php?page=contests) | competitive programming olympiad; Platinum = hard |
| [USACO Guide](https://usaco.guide) | Bronze → Platinum with explanations |
| [CP-Algorithms](https://cp-algorithms.com) | reference proofs + implementations |
| [Codeforces EDU](https://codeforces.com/edu/courses) | segment trees, strings, network flows |
| [LeetCode](https://leetcode.com) | clean single-concept problems |
| [CLRS](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) | *Introduction to Algorithms* — the canonical reference |
| [Go Memory Model](https://go.dev/ref/mem) | the formal spec behind challenge 31 |

**Papers cited in the systems challenges (02–07):**

| Paper | Challenge |
|-------|-----------|
| Dmitry Vyukov — [Non-intrusive MPSC queue](https://www.1024cores.net/home/lock-free-algorithms/queues/non-intrusive-mpsc-node-based-queue) | 02 |
| Boehm — [Can Seqlocks Get Along With Programming Language Memory Models?](https://dl.acm.org/doi/10.1145/2247684.2247688) MSPC 2012 | 03 |
| Chase & Lev — [Dynamic Circular Work-Stealing Deque](https://fzn.fr/readings/ppopp13.pdf) SPAA 2005 | 04 |
| LMAX — [Disruptor Technical Paper](https://lmax-exchange.github.io/disruptor/disruptor.html) | 05 |
| Maged Michael — [Hazard Pointers](https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf) IEEE TPDS 2004 | 06 |
| Herlihy & Shavit — [The Art of Multiprocessor Programming](https://dl.acm.org/doi/10.1145/62527.62529) | 07 |
| Pugh — [Skip Lists: A Probabilistic Alternative](https://dl.acm.org/doi/10.1145/78973.78977) CACM 1990 | 38 |
| Boehm et al. — [Ropes: An Alternative to Strings](https://dl.acm.org/doi/10.1145/214438.214444) 1995 | 39 |

---

## License

Public domain — [Unlicense](UNLICENSE).
