# 21 — KMP String Search

**Task**: Find every position where a pattern P appears in a text T.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

Report every 1-indexed start position where `pattern` occurs in `text`,
including overlapping matches.

The text is long and highly repetitive — up to `|T| = 3·10⁵` characters with a
`|P|` up to `10³`. The obvious scan that re-checks the pattern from scratch
after every mismatch is O(|T|·|P|); on text full of near-matches that almost
complete before failing, it does close to the full product of work and will not
finish in time. Part of the challenge is matching in time linear in the input
size.

Constraints: `|T|` up to 3·10⁵, `|P|` up to 10³, both lowercase a–z (the small
cases also use spaces). `pattern` may be empty — report no positions.

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

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: https://cses.fi/problemset/task/2107
