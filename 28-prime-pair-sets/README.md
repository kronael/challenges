# 28 — Prime Pair Sets

**Task**: Find five primes where every pair — concatenated in either order — is also prime, with the smallest possible sum.

**Difficulty**: expert
**Time estimate**: ~90 min

## Problem

Two primes are "compatible" if both concatenations are prime: 3 and 7 give 37 and
73, both prime. You must find a set of *five* primes, pairwise compatible, whose
sum is minimal. The answer is **26033** (the set {13, 5197, 5701, 6733, 8389}).

The naive search is hopeless: candidates run into the thousands, concatenations
exceed 32 bits, and checking every 5-subset is C(n,5). You need fast primality on
large numbers plus a real clique search with pruning.

## Input / Output

```json
{}
```
Single integer: the smallest sum of a compatible 5-set.

## Examples

**Example 1** — the only case; the whole challenge is one answer.
```
{} → 26033
```

**Why it's hard**: 3‖7 and 7‖3 must *both* be prime, so compatibility is a
symmetric edge in a graph over primes. The answer is the cheapest 5-clique — and
the concatenations grow to 8 digits, killing trial division.

## Teaches

- **Miller–Rabin primality**: deterministic over the 64-bit range, fast enough to test millions of concatenations.
- **Clique search by extension**: backtrack, adding only primes compatible with *every* current member; this pruning is what makes 5-cliques tractable.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [Project Euler #60](https://projecteuler.net/problem=60)
