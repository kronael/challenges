# 42 — Hard — Fragmented String Queries

**Task**: Answer substring queries over the logical concatenation of many string fragments.

**Difficulty**: hard
**Time estimate**: ~70 min

## Problem

You are given an ordered list of string fragments `parts` and a list of
half-open queries `[lo, hi)`. Conceptually the fragments are concatenated, in
order, into one logical string; each query asks for the substring covering
positions `lo` up to but not including `hi` of that logical string. Every
fragment contains ASCII characters only. Positions and lengths are measured in
bytes. Each `lo` and `hi` is clamped to `[0, total]`, where `total` is the
combined byte length. If the clamped range is empty, the answer for that query
is the empty string.

## Input / Output

```json
{"parts": ["abc", "def", "ghi", "jkl"], "queries": [[0, 5], [3, 9], [6, 12]]}
```
Queries use byte offsets in the half-open range `[lo, hi)` and are clamped to
`[0, total]`. Output the extracted substrings joined by `|`.

## Examples

**Example 1** — queries span fragment boundaries.
```
parts ["abc","def","ghi","jkl"], queries [[0,5],[3,9],[6,12]]
  → abcde|defghi|ghijkl
```

**Example 2** — empty slice `[5,5)` yields an empty segment between the bars.
```
parts ["hello","world","foo"], queries [[0,8],[5,5],[2,6]]
  → hellowor||llow
```

## Run

```
make -C rust
make -C python
make -C go
```

Stuck? See `HINTS.md`.
