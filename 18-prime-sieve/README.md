# 18 — Prime Sieve

**Task**: Count how many prime numbers are strictly less than N.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Count the primes strictly below N. For N around 10^8, testing each number for primality — O(N√N) — is far too slow. The insight: instead of asking "is this number prime?", strike out the multiples of every prime you find, so each composite is marked rather than tested.

## Input

```json
{"n": 10}
```

## Output

A single integer: the number of primes `p` with `p < n`.

## Examples

**Example 1** — small case
```
n=10 → 4   (2, 3, 5, 7)
```

**Example 2** — boundary is exclusive, so a prime equal to n is not counted
```
n=2 → 0
```

## Teaches

- **Sieve of Eratosthenes**: mark composites by striking multiples of each prime starting at `p²`; total work is O(n log log n), far below per-number testing.
- **Cache- and memory-aware sieving**: an odd-only bytearray halves space, and for very large `n` a segmented sieve keeps the working set in cache.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: https://projecteuler.net/problem=10
