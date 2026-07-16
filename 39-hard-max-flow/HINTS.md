# Hints — 39 Hard — Max Flow

> Spoilers. Open only when stuck.

- **Residual graph**: give every edge a back-edge with capacity 0. Pushing `d`
  units along an edge subtracts `d` from its residual capacity and adds `d` to
  the back-edge, so flow can be cancelled and re-routed later. A clean trick is
  to store edges in a flat array and pair edge `i` with its reverse `i ^ 1`.
- **Dinic's algorithm** avoids the capacity-dependent worst case of basic
  Ford–Fulkerson. Per phase, a BFS from
  the source labels each node with its distance (level) in the residual graph;
  a DFS then pushes a *blocking flow*, only following edges that go from level
  `k` to level `k+1`. Repeat the BFS/DFS phases until the sink is unreachable.
- **Why O(V²·E) beats O(E·F)**: each phase strictly increases the length of the
  shortest augmenting path, so there are at most `V` phases. Basic
  Ford–Fulkerson may augment the flow by only one unit after an O(E) path search,
  making its running time depend on the maximum flow `F`.
- Keep a per-node iterator pointer during the DFS so dead edges in the current
  phase are skipped, not re-examined.

The `rotten/main.py` reference uses Ford–Fulkerson with a DFS-found augmenting
path. It pushes that path's bottleneck and repeats. The O(E·F) worst case is
correct but TIMEOUTs on the large cases.
