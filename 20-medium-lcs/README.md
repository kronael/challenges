# 20 — Medium — Longest Common Subsequence

**Task**: Find the length of the longest subsequence common to two strings.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Given two strings `s` and `t`, find the length of their longest *common
subsequence*: the longest string of characters that appears in both, in the
same order but not necessarily contiguous. You may delete any characters from
either string, but you may not reorder them.

This is *not* the longest common *substring*: a subsequence may skip over
characters in either string, so `"ABC"` is a subsequence of `"AXBXC"` even
though it never appears as a contiguous block.

Constraints: `|s|`, `|t|` up to a few thousand; characters are printable ASCII.

## Input

```json
{"s": "ABCBDAB", "t": "BDCAB"}
```

## Output

A single integer: the length of the LCS.

## Examples

**Example 1** — characters are shared but scattered across both strings
```
s "ABCBDAB", t "BDCAB" → 4   (e.g. "BDAB" or "BCAB")
```

**Example 2** — substring would give 1; subsequence finds more by skipping
```
s "ABC", t "AXBXC" → 3   ("ABC")
```

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.
