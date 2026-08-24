# 24 — Medium — Cache Eviction

**Task**: Implement a fixed-capacity cache that evicts the least-recently-used key when full, with `get` and `put` both in O(1).

**Difficulty**: medium
**Time estimate**: ~45 min

## Problem

Maintain a cache holding at most `capacity` key→value entries. Process a stream
of operations:

- `get k` — return the stored value for key `k`, or `-1` if `k` is not present.
- `put k v` — set key `k` to value `v`, inserting it if new or overwriting if it
  already exists.

Both `get` and a `put` on an existing key count as *using* that key. When a `put`
inserts a new key and the cache is already at `capacity`, the entry that has gone
untouched the longest (the least recently used) is evicted to make room.

Every `get` and every `put` must run in constant time on average.

Constraints: `1 <= capacity <= 100000`, `0 <= len(ops) <= 400000`. Keys and
values are signed 32-bit integers, so either may be zero or negative.

## Input / Output

```json
{"capacity": 2, "ops": [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2]]}
```
Output the results of the `get` ops only, space-separated, `-1` on a miss (empty
line if there are no gets).

`-1` is not a reserved value: a stored value can itself be `-1`, so a miss and a
hit on a `-1` entry print the same token. Decide presence from the cache, never
from the value.

## Examples

**Example 1** — the `get 1` refreshes key 1, so `put 3` evicts key 2 instead;
`put 4` then evicts key 1, which has become the least recently used.
```
{"capacity":2,"ops":[["put",1,1],["put",2,2],["get",1],["put",3,3],["get",2],["put",4,4],["get",1],["get",3],["get",4]]}
  → 1 -1 -1 3 4
```

**Example 2** — a `put` on an existing key overwrites the value *and* refreshes
recency: rewriting key 2 saves it and dooms key 1, which `put 4` evicts.
```
{"capacity":2,"ops":[["put",2,1],["put",1,1],["put",2,3],["put",4,1],["get",1],["get",2]]}
  → -1 3
```

**Example 3** — three `-1` tokens in a row, and only the middle one is a miss: a
hit on key 1 (which stores `-1`), the evicted key 2, then key 1 again.
```
{"capacity":2,"ops":[["put",1,-1],["put",2,2],["get",1],["put",3,3],["get",2],["get",1],["get",3]]}
  → -1 -1 -1 3
```

## Run

```
make -C rust
make -C go
make -C c
make -C python
```

Stuck? See `hints/01.md`.

Source: [LeetCode 146 — LRU Cache](https://leetcode.com/problems/lru-cache/)
