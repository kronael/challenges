# Hints — 14 Union-Find

> Spoilers. Open only when stuck.

- **Disjoint-set union**: connectivity reduces to "same root". Give every person
  a `parent` pointer (initially itself). Two people are in the same group iff
  walking parents up from each lands on the same root. A merge just points one
  root at the other — turning the relation into pointer chasing.
- **Two tricks together — both needed**: path compression plus union by rank give
  inverse-Ackermann (effectively constant) time per op; neither alone is enough.
  - **Path compression**: after finding a root, re-point every node on the walk
    directly at the root, so the next find is short.
  - **Union by rank (or size)**: when merging, hang the shorter tree under the
    taller one (track an approximate height `rank`, or the subtree size). This
    keeps trees from degrading into long chains.
- A query is then just `find(u) == find(v)` → `1`, else `0`.

The naive approach the problem punishes: storing per-person friend lists and
BFS/DFS-ing on every query, or relabeling an entire group on every merge — both
are O(n) per operation, so O(n·m) overall, which TIMEOUTs on the large cases
(this is what `rotten/main.py` does).

Source: CLRS §21
