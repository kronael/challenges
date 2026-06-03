# 39 — Rope

**Task**: Implement a rope — a binary tree of string fragments — and answer substring queries without materialising the whole string.

**Difficulty**: hard
**Time estimate**: ~70 min

## Problem

A rope stores text as the leaves of a binary tree; concatenation is O(1) (hang two
ropes off a new root) and indexing is O(log n). The naive `s += part` loop is
O(total²) — each `+` recopies the entire prefix — so building a megabyte from
thousands of fragments melts.

The key insight: each internal node stores its left subtree's length (its
*weight*). To index character i, descend left when i < weight, else go right with
i − weight. That weight is what turns linear concatenation into logarithmic
addressing.

## Input / Output

```json
{"parts": ["abc", "def", "ghi", "jkl"], "queries": [[0, 5], [3, 9], [6, 12]]}
```
Queries are half-open `[lo, hi)`, clamped to `[0, total)`. Output the extracted
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

## Teaches

- **Binary tree of fragments**: each internal node stores its left subtree's length (weight); concatenation is O(1).
- **Weight-based traversal**: `extract` descends left when `lo < weight`, right when `hi > weight` (subtracting weight). Build by balanced pairwise merge — a left fold degrades to an O(n) chain.

## Run

```
cd rust   && make
cd python && make
```

Source: [Boehm, Atkinson & Plass, *Ropes: an Alternative to Strings* (1995)](https://www.cs.rit.edu/usr/local/pub/jeh/courses/QUARTERS/FP/Labs/CedarRope/rope-paper.pdf)
