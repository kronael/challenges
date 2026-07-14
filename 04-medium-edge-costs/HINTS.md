# Hints — 04 Medium — Vertex Load Assignment

> Spoilers. Open only when stuck.

- **It's a distance problem.** Each free node's value is forced from below by
  every fixed node: a node `d` hops from an anchor of load `L` must be at least
  `L − d`. The answer at a free node is the pointwise maximum of `L − dist` over
  all anchors, floored at 0.
- **Multi-source propagation**: don't recompute each node against every anchor
  (that's the trap — quadratic in anchors × nodes). Seed all fixed nodes at once
  and let the highest bound win as it spreads.
- **BFS as Dijkstra**: unit edges make this a multi-source BFS / Dijkstra from
  all anchors simultaneously — the same skeleton that scales to weighted graphs.
  Process the largest bound first so each node is settled by its tightest anchor.

The naive method — for each free node, scan every anchor and take the max of
`L − dist` (recomputing distances per pair) — is what `rotten/main.py` does:
correct, but it TIMEOUTs on the large cases.
