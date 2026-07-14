# 16 — Medium — String Search

**Task**: Find every position where a pattern P appears in a text T.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

Report every 1-indexed start position where `pattern` occurs in `text`,
including overlapping matches.

Constraints: `|T|` up to `3 * 10^5`, `|P|` up to `10^3`. Inputs are lowercase
`a`-`z`; one small case includes a space to verify JSON parsing. `pattern` may
be empty; report no positions.

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
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: https://cses.fi/problemset/task/2107
