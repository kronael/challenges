# 09 — Edit Distance

Compute the Levenshtein distance between strings `s` and `t`: the minimum number of single-character insertions, deletions, or substitutions to turn `s` into `t`.

## Input / Output

```
{"s":<string>,"t":<string>}
---
<distance>      minimum number of edits
```

## Examples

```
{"s":"kitten","t":"sitting"}
→ 3

{"s":"flaw","t":"lawn"}
→ 2
```

## Key insight

2-D DP where `dp[i][j]` is the distance between prefixes; each cell is the cheapest of insert/delete/substitute. Two rolling rows give O(|s|·|t|) time, O(min) space.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
