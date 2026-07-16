# 37 — Hard — Prime Pair Sets

**Task**: Find the lowest-sum set of pairwise-compatible primes below a given limit.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

Call two primes *compatible* if concatenating them — in both orders — yields a
prime each time. For example 7 and 109 are compatible because both 7109 and
1097 are prime. The primes 3, 7, 109, and 673 are pairwise compatible, and their
sum, 792, is the lowest sum for any such set of *four* primes.

Given a set size and an exclusive upper bound, find the lowest sum of a set of
primes below that bound that are pairwise compatible. For every pair you pick,
both concatenations must be prime.

## Input / Output

```json
{"size": 5, "limit": 10000}
```
The input is an object with optional `size`, the number of primes to choose, and
optional `limit`, the exclusive upper bound for each chosen prime. They default
to `5` and `10000`. Constraints: `0 <= size <= 5` and `3 <= limit <= 20000`.

Output the smallest possible sum, or `-1` if no such set exists. An empty set
has sum `0`.

## Examples

**Example 1** — full challenge.
```
{"size": 5, "limit": 10000} → 26033
```

**Example 2** — smaller check case.
```
{"size": 4, "limit": 1000} → 792
```

The worked four-prime set above is given only to illustrate the compatibility
rule — your job is the five-prime minimum.

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
