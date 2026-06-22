# 39 — Rope

**Task**: Concatenate many string fragments and answer many overlapping substring queries fast — without materialising the whole joined string for every query.

**Difficulty**: hard
**Time estimate**: ~70 min

## Problem

You are given an ordered list of string fragments `parts` and a list of
half-open queries `[lo, hi)`. Conceptually the fragments are concatenated, in
order, into one logical string; each query asks for the substring covering
positions `lo` up to (but not including) `hi` of that logical string. Each `lo`
and `hi` is clamped to `[0, total]`, where `total` is the combined length. If
the clamped range is empty, the answer for that query is the empty string.

The catch is scale: there can be thousands of fragments and tens of thousands of
queries, and the combined string can run into the megabytes. Naively flattening
the fragments and re-slicing for every query — or rebuilding the joined string
per query — does far too much copying and will not finish in time. The queries
overlap and span fragment boundaries arbitrarily, so you cannot answer them by
touching one fragment at a time either.

## Input / Output

```json
{"parts": ["abc", "def", "ghi", "jkl"], "queries": [[0, 5], [3, 9], [6, 12]]}
```
Queries are half-open `[lo, hi)`, clamped to `[0, total]`. Output the extracted
substrings joined by `|`.

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
cd rust   && make
cd python && make
cd go     && make
```

Stuck? See `HINTS.md`.

Source: [Boehm, Atkinson & Plass, *Ropes: an Alternative to Strings* (1995)](https://www.cs.rit.edu/usr/local/pub/jeh/courses/QUARTERS/FP/Labs/CedarRope/rope-paper.pdf)
