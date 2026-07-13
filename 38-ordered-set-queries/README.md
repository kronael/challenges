# 38 — Ordered Set Queries

**Task**: Maintain an ordered set of integers under inserts, deletes, searches,
and interval-count queries.

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

Maintain a sorted set of integers under a stream of operations:

- `insert v` — add `v` if not already present (duplicates are no-ops).
- `delete v` — remove `v` if present.
- `search v` — is `v` in the set? (emit `1` or `0`).
- `range_count lo hi` — how many stored values lie in the closed interval
  `[lo, hi]`?

Correctness must hold across long mixed streams: duplicate inserts, missing
deletes, negative values, and ranges touching only part of the current set.

Constraints: up to `10^5` operations; values fit in i32; `lo <= hi`.

## Input / Output

```json
{"ops": [["insert", 3], ["search", 4], ["range_count", 2, 5], ["delete", 3]]}
```
`search` emits 1/0, `range_count lo hi` emits the count in `[lo, hi]`; insert and
delete emit nothing.

## Examples

**Example 1** — range_count drops after the delete inside the range.
```
insert 3,1,7,4; search4→1; search5→0; insert2; range_count(2,5)→3; delete3; range_count(2,5)→2
  → 1 0 3 2
```

**Example 2** — operations on an empty list, then a degenerate range.
```
search0→0; range_count(-10,10)→0; insert0; search0→1; range_count(-10,10)→1
  → 0 0 1 1
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.
