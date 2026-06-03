# 35 — LRU Cache

**Task**: Implement a fixed-capacity cache that evicts the least-recently-used key when full, with `get` and `put` both in O(1).

**Difficulty**: medium
**Time estimate**: ~45 min

## Problem

On overflow the cache drops the key untouched for the longest time. The catch is
the dual O(1) requirement. A plain hash map gives O(1) lookup but O(n) to find the
LRU victim. An ordered list gives O(1) eviction but O(n) lookup. Neither alone
works.

The answer is a hash map *plus* a doubly-linked list: the map maps key → node for
O(1) lookup, and the list orders nodes by recency so move-to-front and tail
eviction are both O(1). Every access touches both structures.

## Input / Output

```json
{"capacity": 2, "ops": [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2]]}
```
Output the results of the `get` ops only, space-separated, `-1` on a miss (empty
line if there are no gets).

## Examples

**Example 1** — putting key 3 evicts key 2 (LRU), so its later get misses.
```
cap 2: put1 put2 get1→1 put3 get2→-1 put4 get1→-1 get3→3 get4→4
  → 1 -1 -1 3 4
```

**Example 2** — a `put` on an existing key updates the value *and* refreshes recency.
```
cap 2: put(1,1) put(1,2) get1→2 put2 put(1,3) get1→3 get2→2
  → 2 3 2
```

## Teaches

- **Hash map + doubly-linked list**: map for O(1) lookup, list for O(1) move-to-front and tail eviction; recency *is* the list order, MRU at head.
- **Sentinel nodes**: head/tail sentinels erase the insert/remove end-case branching.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [LeetCode 146 — LRU Cache](https://leetcode.com/problems/lru-cache/)
