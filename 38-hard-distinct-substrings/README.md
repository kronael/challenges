# 38 — Hard — Distinct Substrings

**Task**: Count the number of distinct (unique) substrings of a given string.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

A string of length `n` has `n(n+1)/2` substrings counted by position, but many of
them coincide. Count how many *distinct* non-empty substrings the string has.

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
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

Source: [CSES #2105 — Distinct Substrings](https://cses.fi/problemset/task/2105)
