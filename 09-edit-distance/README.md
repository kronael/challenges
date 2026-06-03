# 09 — Edit Distance

Compute the Levenshtein distance between strings `s` and `t`: the minimum number of single-character insertions, deletions, or substitutions to turn one into the other. The interesting part is recognising the optimal substructure on prefixes and collapsing the DP table to two rows.

**Difficulty: medium** — one classic 2-D DP with a space optimisation, solvable in ~30 min.

## Input / Output

```
{"s":<string>,"t":<string>}
---
<distance>      minimum number of edits
```

## Example

```
{"s":"kitten","t":"sitting"}
→ 3      sitten, sittin, sitting
```

## Teaches

- **2-D dynamic programming**: `dp[i][j]` = distance between prefixes `s[:i]` and `t[:j]`; each cell is the cheapest of insert (`+1`), delete (`+1`), substitute (`+0/1`).
- **Rolling-array space reduction**: only the previous row is needed, cutting space from O(|s|·|t|) to O(min(|s|,|t|)).

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §15.5
