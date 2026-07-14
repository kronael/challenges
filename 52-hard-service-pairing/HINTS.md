# Hints — 52 Hard — Service Pairing

> Spoilers. Open only when stuck.

- This is the assignment problem, or minimum-weight perfect matching in a
  complete bipartite graph.
- The Hungarian, or Kuhn–Munkres, algorithm maintains row and column potentials
  together with a partial matching. For each unmatched row, it finds an
  augmenting path through reduced costs and updates the potentials by the
  smallest unused slack.
- A compact implementation uses arrays `u`, `v`, `p`, and `way`. `p[j]` is the
  row currently matched to column `j`; `way[j]` remembers the previous column
  on the current augmenting path.
- The time cost is `O(n³)` and memory cost is `O(n²)` for the input plus `O(n)`
  working space. Negative costs require no special case.
- The rotten reference tries every permutation of hosts. It is correct but
  needs `n!` placements, so the 12-by-12 benchmark is already out of reach.

Sources:

- Kuhn's 1955 assignment paper:
  https://doi.org/10.1002/nav.3800020109
- Munkres' polynomial-time treatment and transportation extension:
  https://doi.org/10.1137/0105003
