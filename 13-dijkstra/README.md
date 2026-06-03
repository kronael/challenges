# 13 — Dijkstra Shortest Path

Given a directed graph with non-negative edge weights, output the shortest-path distance from node `0` to every node (`-1` if unreachable). The interesting part is the lazy-deletion heap: stale entries are skipped instead of decrease-key'd.

**Difficulty: medium** — one priority-queue graph algorithm with a correctness condition (non-negative weights), solvable in ~30 min.

## Input / Output

```
{"n":<int>,"edges":[[u,v,w],…]}      directed edge u→v with weight w
---
d0 d1 … dn-1      distances from node 0, -1 if unreachable
```

## Example

```
{"n":4,"edges":[[0,1,4],[0,2,1],[2,1,2],[1,3,1]]}
→ 0 3 1 4      0→2→1 (cost 3) beats 0→1 (cost 4)
```

## Teaches

- **Greedy shortest paths with a min-heap**: pop the closest unsettled node and relax its out-edges; once popped a node's distance is final (relies on non-negative weights).
- **Lazy heap deletion**: push improved distances as new entries and discard any pop where `d > dist[u]`, avoiding a decrease-key operation.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §24.3
