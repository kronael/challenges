# 16 — Medium — String Search

**Task**: Find every position where a pattern P appears in a text T.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

Report every 1-indexed start position where `pattern` occurs in `text`,
including overlapping matches.

Constraints: `|T|` is at most `3 * 10^5` and `|P|` is at most `10^3`. Both
strings contain printable ASCII characters, including spaces. `pattern` may be
empty; report no positions.

## Input

```json
{"text": "aababab", "pattern": "abab"}
```

## Output

The 1-indexed start positions in ascending order, space-separated (empty line if none).

## Examples

**Example 1**
```
text "aababab", pattern "abab" → 2 4
```

**Example 2**
```
text "aaaaa", pattern "aa" → 1 2 3 4
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

Source: https://cses.fi/problemset/task/2107
