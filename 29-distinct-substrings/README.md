# 29 — Distinct Substrings

**Task**: Count the number of distinct (unique) substrings of a given string.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

A string of length n has n(n+1)/2 substrings if you count positions; many repeat,
and you want the count of *distinct* ones. Generating them all into a set is
O(n²) substrings of O(n) characters each — quadratic memory, cubic time, dead on
arrival at n = 10⁵.

The trick: build a suffix array, then an LCP array. Every substring is a prefix
of exactly one suffix, and adjacent sorted suffixes share an LCP that counts the
duplicates. The answer falls out of one subtraction.

## Input / Output

```json
{"s": "abab"}
```
Single integer: the number of distinct non-empty substrings (lowercase, n ≤ 10⁵).

## Examples

**Example 1** — overlapping repeats collapse.
```
"abab" → 7      (a, b, ab, ba, aba, bab, abab)
```

**Example 2** — catches a set-based approach that forgets dedup.
```
"aaa" → 3       (a, aa, aaa) — not 6
```

## Teaches

- **Suffix array (O(n log n))**: sort all suffixes by prefix doubling; every substring is a prefix of one suffix.
- **Kasai's LCP**: longest common prefix of adjacent sorted suffixes in O(n), reusing the previous value.
- **The formula**: total prefixes `n(n+1)/2` minus `Σ LCP` removes exactly the double-counted shared prefixes.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [CSES #2105 — Distinct Substrings](https://cses.fi/problemset/task/2105)
