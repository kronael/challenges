# 38 — Skip List

**Task**: Implement a skip list supporting insert, delete, search, and range-count, all in expected O(log n).

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

Maintain a sorted multiset of integers under a stream of operations, answering
each query in expected O(log n):

- `insert v` — add `v` if not already present (duplicates are no-ops).
- `delete v` — remove `v` if present.
- `search v` — is `v` in the set? (emit `1` or `0`).
- `range_count lo hi` — how many stored values lie in the closed interval
  `[lo, hi]`?

A skip list is the structure named by this challenge: a sorted linked list
augmented so that lookups need not walk every node. The catch is that its balance
is *probabilistic*, not structural — there are no rotations to fall back on, and
correctness must hold for any random choices the structure makes internally. A
query that descends or splices a pointer one step wrong does not crash; it
silently loses elements and returns a subtly wrong count. With up to `10^5`
operations, the naive "rescan the whole list every time" approach is too slow.

Constraints: up to `10^5` operations; values fit in i32.

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
cd python && make
```

Stuck? See `HINTS.md`.

Source: [Pugh, *Skip Lists: A Probabilistic Alternative to Balanced Trees* (CACM 1990)](https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf)
