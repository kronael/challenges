# 06 — Medium — Edit Distance

**Task**: Implement the core of a spell-checker: the fewest single-character edits to turn a misspelled word into the intended one.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

A user typed `s`; you think they meant `t`. Compute the minimum number of
single-character edits — insert, delete, or replace — that transforms `s` into
`t`. This is the number a spell-checker uses to rank suggestions.

Constraints:

- `0 <= |s|, |t| <= 4000`
- `s` and `t` contain only lowercase ASCII letters.

## Input

```json
{"s": "kitten", "t": "sitting"}
```

## Output

A single integer: the minimum number of edits.

## Examples

**Example 1** — kitten → sitten, replace → sittin, replace → sitting, insert
```
{"s":"kitten","t":"sitting"} → 3
```

**Example 2** — when one string is empty, every char of the other is an insert
```
{"s":"","t":"abc"} → 3
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.
