# 21 — KMP String Search

Report every 1-indexed start position where `pattern` occurs in `text`. The challenge is matching in O(n+m) by never re-examining a character after a mismatch.

## Input / Output

```
{"text":<string>,"pattern":<string>}
---
p1 p2 …      1-indexed start positions, ascending (empty line if none)
```

## Example

```
{"text":"aababab","pattern":"abab"}
→ 2 4
```

## Teaches

- **Failure function**: precompute, for each prefix, the longest proper prefix that is also a suffix; on a mismatch this tells you how far to fall back instead of restarting.
- **Linear matching (and the Z-function)**: the text pointer never moves backward, giving O(n+m); the related Z-function answers "how far does the match extend from here".

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: https://cses.fi/problemset/task/2107
