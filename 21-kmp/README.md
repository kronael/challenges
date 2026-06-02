# 21 — KMP String Search

Find every occurrence of `pattern` inside `text` and report the 1-indexed start positions.

## Input / Output

```
{"text":<string>,"pattern":<string>}
---
p1 p2 …      1-indexed start positions, ascending (empty line if none)
```

## Examples

```
{"text":"aababab","pattern":"abab"}
→ 4

{"text":"aaaa","pattern":"aa"}
→ 1 2 3
```

## Key insight

Build the KMP failure function (longest proper prefix that is also a suffix) for the pattern in O(m), then scan the text once in O(n), never re-examining a matched character: total O(n+m).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
