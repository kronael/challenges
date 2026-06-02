# 38 — Skip List

Implement a **skip list** — a probabilistic, multi-level linked list that gives
expected `O(log n)` search, insert, and delete without the rotations of a
balanced BST. Process a stream of operations and answer the queries.

Operations:

- `insert(val)` — add `val` (ignore duplicates).
- `delete(val)` — remove `val` if present.
- `search(val)` → `1` if present, else `0`.
- `range_count(lo, hi)` → number of stored elements in `[lo, hi]` inclusive.

## Input / Output

```
{"ops":[["insert",3],["search",3],["range_count",1,5],…]}
---
r0 r1 …      results of search and range_count ops, in order, space-separated
```

`search` emits `1`/`0`; `range_count` emits the count. `insert` / `delete`
emit nothing.

## Examples

```
{"ops":[["insert",3],["insert",1],["insert",7],["insert",4],["search",4],
        ["search",5],["insert",2],["range_count",2,5],["delete",3],
        ["range_count",2,5]]}
→ 1 0 3 2
```

After the four inserts the set is `{1,3,4,7}`: `search(4)=1`, `search(5)=0`.
Add `2` → `{1,2,3,4,7}`: `range_count(2,5)=3` (`2,3,4`). Delete `3` →
`{1,2,4,7}`: `range_count(2,5)=2` (`2,4`).

## Constraints

- up to `10⁴` operations
- values in `[-10⁵, 10⁵]`

Large case: 50k inserts followed by 50k search / range_count queries.

## Notes

A node's height is chosen by flipping a coin until tails (`P = 0.5`), capped at
`MAX_LEVEL`. Search/insert/delete walk from the top level down, dropping a level
whenever the next node would overshoot. The output is defined purely by the set
of stored values, so it does not depend on the random level choices — any PRNG
seed gives the same answers. Use a fixed seed for reproducible benchmarks.

Source: https://www.baeldung.com/cs/skip-lists ·
https://www.geeksforgeeks.org/dsa/skip-list/

## Run

```
cd rust   && make test && make bench
cd python && make test && make bench
```

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.
