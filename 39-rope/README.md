# 39 — Rope

A rope is a binary tree of string fragments; build one from `parts` and answer substring queries `[lo, hi)` without materialising the whole string.
Hard because a naive `s += part` loop is O(total²) (each `+` recopies the prefix); the rope builds in O(n log n) and slices in O(log n + k) via weight-based indexing.

## Input / Output
```
{"parts":["abc","def",…], "queries":[[lo,hi],…]}      half-open, clamped to [0, total)
---
sub0|sub1|…    extracted substrings joined by '|'
```

## Teaches

- **Binary tree of fragments**: each internal node stores its left subtree's length (its weight); concatenation is O(1) — just hang two ropes off a new root.
- **Weight-based traversal**: `extract` descends left when `lo < weight`, right when `hi > weight` (subtracting weight). Build by balanced pairwise merge, not a left fold (which degrades to an O(n) chain).

## Run
```
cd rust   && make
cd python && make
```
Source: [Boehm, Atkinson & Plass, *Ropes: an Alternative to Strings* (1995)](https://www.cs.rit.edu/usr/local/pub/jeh/courses/QUARTERS/FP/Labs/CedarRope/rope-paper.pdf)
