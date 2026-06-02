# 28 — Prime Pair Sets (Project Euler #60)

The primes 3, 7, 109, 673 are remarkable: concatenating any two in either order yields a prime (3‖7=37, 7‖3=73, …). Find the lowest sum of a set of **five** primes for which every pair concatenates to a prime in both orders.

## Input / Output

```
{}            no input
---
<int>         the lowest such sum
```

## Examples

```
{}
→ 26033        the set {13, 5197, 5701, 6733, 8389}
```

## Key insight

Build a graph whose nodes are primes and whose edge `(p,q)` exists iff both `p‖q` and `q‖p` are prime; the answer is the cheapest 5-clique. Backtracking that only extends with primes pairwise-compatible with the current set prunes the search hard.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```

Source: [projecteuler.net/problem=60](https://projecteuler.net/problem=60)
