# 29 — Distinct Substrings

**Task**: Count the number of distinct (unique) substrings of a given string.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

A string of length `n` has `n(n+1)/2` substrings counted by position, but many of
them coincide. Count how many *distinct* non-empty substrings the string has.

The naive route — generate every substring and drop it into a set — is `O(n²)`
substrings of up to `O(n)` characters each, so it is quadratic in memory and
cubic in time. At `n = 10⁵` it never finishes and never fits; clearing that wall
is the point of the challenge.

Constraints: `1 ≤ n ≤ 10⁵`, characters are lowercase `a`–`z`. The answer can
exceed a 32-bit integer.

## Input / Output

```json
{"s": "abab"}
```
Single integer: the number of distinct non-empty substrings.

## Examples

**Example 1** — overlapping repeats collapse.
```
"abab" → 7      (a, b, ab, ba, aba, bab, abab)
```

**Example 2** — duplicates must not be counted twice.
```
"aaa" → 3       (a, aa, aaa) — not 6
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: [CSES #2105 — Distinct Substrings](https://cses.fi/problemset/task/2105)
