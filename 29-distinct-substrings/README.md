# 29 — Distinct Substrings

Count the distinct non-empty substrings of a lowercase string (length up to 10⁵).
Hard because the naive set-of-substrings is O(n²) substrings; you need a suffix array and LCP array to count them in O(n log n).

## Input / Output
```
{"s":<string>}
---
<int>      number of distinct substrings   ("abab" → 7, "aaa" → 3)
```

## Teaches

- **Suffix array in O(n log n)**: sort all suffixes by prefix-doubling; every substring is a prefix of exactly one suffix.
- **Kasai's LCP algorithm**: longest common prefixes of adjacent sorted suffixes in O(n), reusing the previous LCP.
- **The counting formula**: total prefixes `n(n+1)/2` minus `Σ LCP` removes the double-counted shared prefixes.

## Run
```
cd rust   && make
cd go     && make
cd python && make
```
Source: [CSES #2105 — Distinct Substrings](https://cses.fi/problemset/task/2105)
