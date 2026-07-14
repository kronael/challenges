# Hints — 18 Medium — Topological Sort

> Spoilers. Open only when stuck.

- **Kahn's BFS by in-degree**: compute each node's in-degree (number of
  prerequisites). Repeatedly emit a node whose in-degree is 0 and decrement the
  in-degree of each of its successors; when a successor drops to 0 it becomes
  ready. This visits every node and edge once — O(n + e).
- **Smallest ready node first**: keep the ready nodes (in-degree 0) in a
  min-heap instead of a plain queue. Popping the minimum each step yields the
  lexicographically smallest valid order without ever re-scanning the graph.
- **Cycle = leftover nodes**: a cycle's nodes never reach in-degree 0, so they
  are never emitted. If fewer than `n` nodes come out, the rest form a cycle —
  output `CYCLE`. Cycle detection falls out of the ordering for free.

The naive approach — at each step scanning all `n` nodes to find the smallest
one with no remaining prerequisites — is O(n²) and TIMEOUTs on the large cases;
that is what `rotten/main.py` does.

Source: CLRS §22.4
