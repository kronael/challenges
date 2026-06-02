# 29 — Distinct Substrings (CSES #2105)

Given a lowercase string `s` (length up to 10⁵), count the number of distinct non-empty substrings.

## Input / Output

```
{"s":<string>}
---
<int>      number of distinct substrings
```

## Examples

```
{"s":"abab"}
→ 7

{"s":"aaa"}
→ 3
```

## Key insight

Build the suffix array and the LCP array (Kasai). Every substring is a prefix of some suffix; the total number of prefixes is `n(n+1)/2`, and adjacent suffixes in sorted order share `LCP` prefixes that would be double-counted, so the answer is `n(n+1)/2 − Σ LCP`.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```

Source: [cses.fi/problemset/task/2105](https://cses.fi/problemset/task/2105)
