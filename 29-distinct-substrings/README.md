# 29 — Distinct Substrings (CSES #2105)

Given a string of length n (1 ≤ n ≤ 10⁵, lowercase a–z), count the number
of **distinct substrings**.

## Input / Output

```
abab
---
6
```

(Distinct substrings of "abab": a, ab, aba, abab, b, ba, bab, bab — wait,
without duplicates: a, ab, aba, abab, b, ba, bab = 7. But "a" appears twice
as a substring position, counted once.)

## Key idea

Build the suffix array in O(n log n). Compute the LCP array with Kasai's
algorithm. Answer = n(n+1)/2 − sum(LCP). Each LCP value removes the shared
prefixes that would otherwise be double-counted as distinct substrings.

## Input / Output format

```
Stdin:  one string
Stdout: one integer
```

```
cd go   && make test
cd rust && make test
```

Source: [cses.fi/problemset/task/2105](https://cses.fi/problemset/task/2105)
