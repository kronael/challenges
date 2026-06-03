# 27 — Longest Common Subsequence

Find the length of the longest subsequence common to two strings (in order, not necessarily contiguous). The challenge is the 2-D dependency between prefixes of both strings.

## Input / Output

```
{"s":<string>,"t":<string>}
---
<int>      length of the LCS
```

## Example

```
{"s":"ABCBDAB","t":"BDCAB"}
→ 4      (e.g. "BDAB" or "BCAB")
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
