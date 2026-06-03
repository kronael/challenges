# 18 — Prime Sieve

Count the primes strictly below `n`. The challenge is staying fast as `n` grows to `10^8`, where trial division per number dies.

## Input / Output

```
{"n":<int>}
---
<count>      number of primes p with p < n
```

## Example

```
{"n":10}
→ 4      (2, 3, 5, 7)
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
