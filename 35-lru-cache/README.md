# 35 — LRU Cache

Fixed-capacity least-recently-used cache: `get`/`put` in O(1), evicting the least-recently-used key on overflow.
Medium because O(1) on both operations forces the hash-map-plus-doubly-linked-list pairing — neither structure alone gives both O(1) lookup and O(1) recency reordering.

## Input / Output
```
{"capacity":<int>, "ops":[["get",k] | ["put",k,v], …]}
---
space-separated results of the get ops only, -1 on miss (empty line if no gets)
```

## Teaches

- **Hashmap + doubly-linked list**: the map gives O(1) lookup, the list gives O(1) move-to-front and tail eviction; recency is the list order (MRU at head).
- **Sentinel nodes**: head/tail sentinels remove all the insert/remove end-case branching.

## Run
```
cd rust   && make
cd go     && make
cd python && make
```
Source: [LeetCode 146 — LRU Cache](https://leetcode.com/problems/lru-cache/)
