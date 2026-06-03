# 27 — Longest Common Subsequence

**Task**: Find the length of the longest subsequence common to two strings.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Find the longest common subsequence of two strings — the longest run of characters that appears in both, in order but not necessarily contiguous. This is *not* the longest common substring: a subsequence may skip characters in either string. The trick is filling a 2-D grid indexed by prefixes of both strings, where each cell builds on the cells above, left, and diagonal.

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

## Teaches

- **2-D prefix DP**: `dp[i][j]` is the LCS of the first `i` chars of `s` and first `j` of `t`; a match extends the diagonal, otherwise take the better of dropping one character.
- **Rolling rows**: each row depends only on the previous one, so two rows give O(|s|·|t|) time in O(min(|s|,|t|)) space.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: CLRS §15.4
