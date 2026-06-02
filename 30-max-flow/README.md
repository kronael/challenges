# 30 — Max Flow / Min Cut (CSES #1694 — Download Speed)

n computers (1 ≤ n ≤ 500), m directed connections (1 ≤ m ≤ 1000), each with
integer capacity c (1 ≤ c ≤ 10⁹). Find the **maximum flow** from node 1 to
node n.

## Input / Output

```
4 5
1 2 3
2 4 2
1 3 4
3 4 5
4 1 3
---
6
```

## Key ideas

- Implement Dinic's algorithm: BFS to build level graph, DFS to push blocking
  flow. Time O(V² × E), fast in practice.
- Correctness: max-flow = min-cut (Ford-Fulkerson theorem). The min cut
  partitions nodes into two sets; verify it equals the flow value.

## Input / Output format

```
Stdin:  n m, then m lines: a b c
Stdout: one integer (max flow)
```

```
cd go   && make test
cd rust && make test
```

Source: [cses.fi/problemset/task/1694](https://cses.fi/problemset/task/1694)
