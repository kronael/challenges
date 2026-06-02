# 18 — Prime Sieve

Count the prime numbers strictly below `n`.

## Input / Output

```
{"n":<int>}
---
<count>      number of primes p with p < n
```

## Examples

```
{"n":10}
→ 4

{"n":1000000}
→ 78498
```

## Key insight

Sieve of Eratosthenes: mark composites by striking out multiples of each prime starting at `p²`. An odd-only bytearray sieve handles `n = 10^8` in seconds; the naive trial-division-per-number approach is far slower.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
