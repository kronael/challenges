# Hints — 35 LRU Cache

> Spoilers. Open only when stuck.

- **Hash map + doubly-linked list**: a plain hash map gives O(1) lookup but O(n)
  to find the LRU victim; an ordered list gives O(1) eviction but O(n) lookup.
  Neither alone works. Use both together: the map maps key → node for O(1)
  lookup, and the list orders nodes by recency so move-to-front and tail eviction
  are both O(1). Every access touches both structures — recency *is* the list
  order, with the most-recently-used node at the head.
- **Sentinel nodes**: keep dummy head/tail nodes so insert and remove never have
  to special-case the empty list or the ends — every real node always has a
  `prev` and a `next`. This erases the end-case branching.
- On a `get` hit and on a `put` to an existing key, unlink the node and push it to
  the front. On a `put` that overflows capacity, evict `tail.prev` (the LRU) and
  drop its key from the map.

The trap is any approach that scans the cache to find the eviction victim — e.g.
tracking a per-key "last used" timestamp and scanning for the minimum on each
overflow. That is correct but O(n) per eviction, which TIMEOUTs on the large
cases (see `rotten/`).
