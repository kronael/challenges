# 09 — Edit Distance

**Task**: Implement the core of a spell-checker: the fewest single-character edits to turn a misspelled word into the intended one.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

A user typed `s`; you think they meant `t`. Compute the minimum number of single-character edits — insert, delete, or replace — that transforms `s` into `t`. This is the Levenshtein distance, the number a spell-checker uses to rank suggestions.

The greedy "fix the first mismatch" instinct fails: sometimes deleting is cheaper than replacing, and you can't know which without looking ahead. The fix is a DP over prefixes — and once it works, you'll notice you only ever read the previous row.

Constraints: |s|, |t| up to a few thousand.

## Input

```json
{"s": "kitten", "t": "sitting"}
```

## Output

A single integer: the minimum number of edits.

## Examples

**Example 1** — kitten → sitten (replace) → sittin (replace) → sitting (insert)
```
{"s":"kitten","t":"sitting"} → 3
```

**Example 2** — when one string is empty, every char of the other is an insert
```
{"s":"","t":"abc"} → 3
```

## Teaches

- **2-D dynamic programming**: `dp[i][j]` = distance between prefixes `s[:i]` and `t[:j]`; each cell is the cheapest of insert (+1), delete (+1), or substitute (+0/1).
- **Rolling-array space**: only the previous row is needed, so space drops from O(|s|·|t|) to O(min(|s|,|t|)).

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §15.5
