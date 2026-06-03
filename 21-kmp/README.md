# 21 — KMP String Search

**Task**: Find every position where a pattern P appears in a text T.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

Report every 1-indexed start position where `pattern` occurs in `text`, including overlapping matches. The naive approach re-checks the pattern from scratch on every mismatch — O(|T|·|P|), which blows up on long repetitive text. You need O(|T|+|P|): precompute a failure function so the text pointer never moves backward.

## Input

```json
{"text": "aababab", "pattern": "abab"}
```

## Output

The 1-indexed start positions in ascending order, space-separated (empty line if none).

## Examples

**Example 1** — overlapping matches share characters
```
text "aababab", pattern "abab" → 2 4
```

**Example 2** — the case that wrecks the naive scan: many near-matches before each real one
```
text "aaaaa", pattern "aa" → 1 2 3 4
```

## Teaches

- **Failure function**: for each prefix, the longest proper prefix that is also a suffix; on a mismatch this tells you how far to fall back instead of restarting.
- **Linear matching**: the text pointer never moves backward, giving O(n+m); the related Z-function answers "how far does the match extend from here".

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: https://cses.fi/problemset/task/2107
