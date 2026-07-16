# Hints — 55 Hard — Changing Network Queries

> Spoilers. Open only when stuck.

- Pair each `add` with its `remove`. Every edge is active over one or more time
  intervals. Edges left active at the end run through the end of the sequence.
- Put each active interval into a segment tree over operation indices. An edge
  belongs to every tree node whose time range is fully covered by its interval.
- Traverse the tree with a disjoint-set union structure that supports rollback.
  Apply a node's edges on entry and undo them on exit.
- Do not use path compression in a rollback DSU. Union by size keeps trees
  shallow, while a stack of parent and size changes makes rollback constant per
  successful union.
- Rebuilding adjacency and searching the live graph for every query is correct
  but can take quadratic work. That is the rotten reference.

Further reading: [Holm, de Lichtenberg, and Thorup — Fully dynamic graph
connectivity](https://doi.org/10.1145/276698.276715) studies the online version
of the problem. It does not use the offline method described above.
