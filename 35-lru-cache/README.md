# 35 — LRU Cache

Implement a fixed-capacity Least-Recently-Used cache and replay a stream of
operations against it.

- `["get", k]` — return the value for key `k`, or `-1` if absent. A hit counts
  as a use (`k` becomes most-recently-used).
- `["put", k, v]` — insert or overwrite `k → v` (a use). If this pushes the
  size past `capacity`, evict the least-recently-used key first.

Both `get` and `put` must run in `O(1)`. The intended structure is a hash map
from key to a node in a doubly linked list ordered by recency (MRU at the head,
LRU at the tail): the map gives `O(1)` lookup, the list gives `O(1)` move-to-
front and tail eviction. No built-in ordered map or LRU library.

## Input

```json
{"capacity": 2,
 "ops": [["put",1,1],["put",2,2],["get",1],["put",3,3],["get",2],
         ["put",4,4],["get",1],["get",3],["get",4]]}
```

`1 ≤ capacity ≤ 3000`, up to `10⁴` ops, keys and values are positive integers.

## Output

Space-separated results of the `get` operations only, in order (`-1` for a
miss). If there are no gets, the output is an empty line.

```
1 -1 -1 3 4
```

## Example

```
{"capacity":2,"ops":[["put",1,1],["put",2,2],["get",1],["put",3,3],
                     ["get",2],["put",4,4],["get",1],["get",3],["get",4]]}
→ 1 -1 -1 3 4
```

After `put 3` evicts key 2 (LRU), so `get 2` → -1; then `put 4` evicts key 1,
so `get 1` → -1; `get 3` → 3 and `get 4` → 4 survive.

## Key insight

Keep a sentinel-bounded doubly linked list so insert/remove never special-case
the ends. Every `get` hit and every `put` moves its node to the head. On a `put`
that overflows capacity, unlink the tail node and drop its key from the map.

Source: [LeetCode 146 — LRU Cache](https://leetcode.com/problems/lru-cache/)

## Run

```
cd rust   && make test && make bench
cd go     && make test && make bench
cd python && make test && make bench
```

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.
