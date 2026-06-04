# Hints — 30 Max Flow

> Spoilers. Open only when stuck.

- **Residual graph**: give every edge a back-edge with capacity 0. Pushing `d`
  units along an edge subtracts `d` from its residual capacity and adds `d` to
  the back-edge, so flow can be cancelled and re-routed later. A clean trick is
  to store edges in a flat array and pair edge `i` with its reverse `i ^ 1`.
- **Dinic's algorithm** beats plain Ford–Fulkerson here. Per phase: a BFS from
  the source labels each node with its distance (level) in the residual graph;
  a DFS then pushes a *blocking flow*, only following edges that go from level
  `k` to level `k+1`. Repeat the BFS/DFS phases until the sink is unreachable.
- **Why O(V²·E) beats O(V·E²)**: each phase strictly increases the length of the
  shortest augmenting path, so there are at most `V` phases. Plain
  Ford–Fulkerson augments one arbitrary path at a time and can take far more
  rounds on adversarial graphs (long thin augmenting paths) — that is the trap
  the large cases punish.
- Keep a per-node iterator pointer during the DFS so dead edges in the current
  phase are skipped, not re-examined.

The naive plain-Ford–Fulkerson approach (BFS for any augmenting path, push its
bottleneck, repeat) is what `rotten/main.py` does — correct, but it TIMEOUTs on
the large cases.
