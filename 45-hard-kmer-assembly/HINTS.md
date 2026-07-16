# Hints — 45 Hard — K-mer Assembly

> Spoilers. Open only when stuck.

- **De Bruijn graph**: make each k-mer an *edge*, not a node. The edge runs from
  its length-`(k-1)` prefix to its length-`(k-1)` suffix. So `GGCT` is an edge
  `GGC → GCT`. Every (k-1)-mer that appears is a node; the k-mers are the
  directed edges connecting them. Reconstructing the genome = walking every edge
  exactly once: an **Eulerian path**.
- **Hash the nodes to ints**: don't key the graph on string (k-1)-mers — intern
  each distinct (k-1)-mer to a small integer (a dict / map from string to id),
  and store the adjacency as `list[list[int]]`. Building this is O(n·k).
- **Find the start node**: an Eulerian path starts at the node with
  `outdegree − indegree = +1` (one more edge leaving than entering). If every
  node is balanced (a cycle), start anywhere. Track `outdeg[v] − indeg[v]` per
  node while building.
- **Hierholzer's algorithm**, O(edges): iterative DFS. Push the start node on a
  stack; while the stack is non-empty, if the top node still has an unused
  outgoing edge, follow it (advance a per-node pointer into its adjacency list)
  and push the target; otherwise pop the node onto the output path. Reverse the
  output path at the end — that's the Eulerian node sequence.
- **Spell the genome**: the walk visits `n + 1` nodes. Emit the full first node
  ((k-1) chars), then for each subsequent node append only its *last* character.
  Result length = `n + k − 1`.

A correct naive baseline tries every k-mer occurrence as the first fragment and
backtracks over the rest. At each step, try every unused k-mer whose prefix
matches the current suffix, and accept a branch only after it uses every
occurrence. This exhaustive edge-order search is correct, but exponential on
ambiguous prefixes and unsuitable for the large cases.

Related sources:

- [Rosalind — Genome Assembly with Perfect Coverage](https://rosalind.info/problems/pcov/)
  studies the related circular case under a simple-cycle guarantee. This
  challenge instead asks for a unique linear reconstruction.
- [Compeau, Pevzner, and Tesler — How to apply de Bruijn graphs to genome
  assembly](https://doi.org/10.1038/nbt.2023) gives the broader genome-assembly
  context.
