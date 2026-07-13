# 18 — Count Primes

**Task**: Count how many prime numbers are strictly less than N.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Count the primes strictly below `n`. A prime equal to `n` is not counted.

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

Source: https://leetcode.com/problems/count-primes/
