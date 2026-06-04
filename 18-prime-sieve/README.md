# 18 — Prime Sieve

**Task**: Count how many prime numbers are strictly less than N.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Count the primes strictly below `n`. A prime equal to `n` is not counted.

`n` reaches 10^8, so the answer must come back fast. Testing each candidate for
primality one at a time — checking divisors up to its square root — is O(n√n)
and will not finish in time at that scale; part of the challenge is finding a
formulation that does, while keeping the working set small enough to stay in
memory.

Constraints: `n` up to 10^8.

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

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: https://projecteuler.net/problem=10
