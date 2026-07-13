# Hints — 13 Dijkstra Shortest Path

> Spoilers. Open only when stuck.

- **Greedy shortest paths with a min-heap**: keep a tentative distance for every
  node, all `-1` (unreached) except the source at `0`. Repeatedly pop the nearest
  unsettled node off a min-heap and relax its out-edges — for each edge `u → v`
  with weight `w`, if `dist[u] + w` beats `dist[v]`, lower `dist[v]` and push it.
  Because every weight is non-negative, the moment a node is popped its distance
  is final (no later, longer path can improve it) — which is also exactly why a
  negative weight would break it.
- **Lazy heap deletion**: instead of a decrease-key, push the improved distance as
  a fresh `(d, u)` entry and skip any pop where `d > dist[u]` (a stale duplicate).
  This keeps the heap simple and runs in O((n + m) log n).
- **Why the obvious thing is too slow**: scanning all nodes each round to find the
  current minimum is O(n²) — fine on the examples, hopeless at n = 10⁵. The heap
  is what turns the round-by-round minimum search into a log-factor operation.

Source: CLRS §24.3
