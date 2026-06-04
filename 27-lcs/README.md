# 27 — Longest Common Subsequence

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

The strings are long — up to a few thousand characters each — and the answer
must come back fast. The obvious recursive formulation (at each mismatch, try
dropping a character from one side or the other and take the better result)
re-explores the same pairs of prefixes over and over; its running time blows up
exponentially and it will not finish at this scale. Part of the challenge is
finding a formulation that does.

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

Source: CLRS §15.4 (longest common subsequence)
