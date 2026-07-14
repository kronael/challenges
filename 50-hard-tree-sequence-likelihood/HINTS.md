# Hints — 50 Hard — Tree Sequence Likelihood

> Spoilers. Open only when stuck.

- Use Felsenstein's pruning algorithm, a bottom-up dynamic program on the tree.
- For each node and possible base, keep the probability of all observations in
  that node's subtree conditioned on the node having that base.
- At a leaf, the observed base has conditional probability one and the other
  three bases have probability zero. At an internal node, combine a child by
  summing over the child's four possible bases, then multiply the independent
  child contributions.
- Work in log space. Multiplication becomes addition, while each sum uses the
  log-sum-exp operation. This avoids underflow on deep trees.
- Process one alignment site at a time. The time cost is `O(sites · edges · 4²)`
  and the working memory is `O(nodes · 4)`.
- The rotten reference enumerates all four-base assignments to every internal
  node. A binary tree with 15 internal nodes already requires `4¹⁵` assignments
  per site.

Sources:

- Felsenstein's original maximum-likelihood DNA tree paper:
  https://doi.org/10.1007/BF01734359
- A retrospective explaining the pruning calculation and its influence:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7803665/
