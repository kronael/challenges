# 28 — Prime Pair Sets

**Task**: Find a set of five primes such that any two of them, concatenated in either order, also form a prime — and whose sum is the smallest possible.

**Difficulty**: expert
**Time estimate**: ~90 min

## Problem

Call two primes *compatible* if concatenating them — in both orders — yields a
prime each time. For example 7 and 109 are compatible because both 7109 and
1097 are prime. The primes 3, 7, 109, and 673 are pairwise compatible, and their
sum, 792, is the lowest sum for any such set of *four* primes.

Find the lowest sum for a set of *five* primes that are pairwise compatible: for
every pair you pick, both concatenations must be prime.

The search space is brutal. The five primes are not small, so the candidate pool
runs into the thousands and the number of 5-subsets is astronomical. The
concatenations grow past eight digits, so any primality test that trial-divides
will fall over. Both the candidate explosion and the size of the numbers being
tested have to be tamed for the search to finish.

## Input / Output

```json
{}
```
The input is the empty object. Output a single integer: the smallest sum of a
pairwise-compatible set of five primes.

## Examples

**Example 1** — the only case; the whole challenge is one answer.
```
{} → 26033
```

The worked four-prime set above (sum 792) is given only to illustrate the
compatibility rule — your job is the five-prime minimum.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: [Project Euler #60](https://projecteuler.net/problem=60)
