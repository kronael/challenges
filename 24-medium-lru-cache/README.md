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

Constraints: `1 <= capacity <= 3000`, up to 2·10⁵ operations, keys and values
fit in i32.

## Input / Output

```json
{"capacity": 2, "ops": [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2]]}
```
Output the results of the `get` ops only, space-separated, `-1` on a miss (empty
line if there are no gets).

## Examples

**Example 1** — putting key 3 evicts key 2, so its later get misses.
```
cap 2: put1 put2 get1→1 put3 get2→-1 put4 get1→-1 get3→3 get4→4
  → 1 -1 -1 3 4
```

**Example 2** — a `put` on an existing key updates the value *and* refreshes recency.
```
cap 2: put(1,1) put(1,2) get1→2 put2 put(1,3) get1→3 get2→2
  → 2 3 2
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

Source: [LeetCode 146 — LRU Cache](https://leetcode.com/problems/lru-cache/)
