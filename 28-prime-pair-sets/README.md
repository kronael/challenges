# 28 — Prime Pair Sets

Find the lowest sum of five primes where concatenating any two in either order is also prime (e.g. 3‖7=37, 7‖3=73).
Hard because it fuses fast primality testing with a clique search: the answer is the cheapest 5-clique in a graph whose edges are "both concatenations are prime".

## Input / Output
```
{}            no input
---
<int>         lowest such sum   (e.g. 26033 for {13, 5197, 5701, 6733, 8389})
```

## Teaches

- **Miller-Rabin primality**: deterministic for the 64-bit range used here, fast enough to test millions of concatenations.
- **Clique search by pairwise extension**: backtrack extending the set only with primes compatible with *every* member so far; this pruning is what makes the search tractable.

## Run
```
cd rust   && make
cd go     && make
cd python && make
```
Source: [Project Euler #60](https://projecteuler.net/problem=60)
