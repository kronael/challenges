# 27 — Longest Common Subsequence

Given two strings `s` and `t`, find the length of their longest common subsequence (characters in order but not necessarily contiguous).

## Input / Output

```
{"s":<string>,"t":<string>}
---
<int>      length of the LCS
```

## Examples

```
{"s":"ABCBDAB","t":"BDCAB"}
→ 4

{"s":"abc","t":"xyz"}
→ 0
```

## Key insight

2D DP: `dp[i][j]` = LCS of the first `i` chars of `s` and first `j` of `t`. On a match extend the diagonal, else take the better of dropping one character. Two rolling rows give O(|s|·|t|) time, O(min) space.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
