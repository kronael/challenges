# Hints — 42 Hard — Rope

> Spoilers. Open only when stuck.

- **Binary tree of fragments**: store the text as the leaves of a binary tree.
  Concatenation is O(1) — hang two ropes off a new root — and indexing is
  O(log n). Each internal node stores its left subtree's length (its *weight*).
- **Weight-based traversal**: to index character `i`, descend left when
  `i < weight`, else go right with `i − weight`. For an `[lo, hi)` extract,
  recurse left when `lo < weight` (clamping `hi` to `weight`) and right when
  `hi > weight` (subtracting `weight` from both bounds), appending whole leaf
  slices as you reach them. That weight is what turns linear concatenation into
  logarithmic addressing, and batching per-leaf slices avoids touching one
  character at a time.
- **Build balanced**: merge the fragments by repeated pairwise merge so the tree
  has O(log n) depth. A naive left fold builds a degenerate O(n) right-leaning
  chain, and every index/extract then walks that whole chain.

The naive approach in `rotten/main.py` — building a degenerate chain and
indexing it one character per query, or re-flattening/re-joining the whole
string per query — is correct but TIMEOUTs on the large cases. `rotten/main.py`
does this.

Source: [Boehm, Atkinson & Plass, *Ropes: an Alternative to Strings* (1995)](https://www.cs.rit.edu/usr/local/pub/jeh/courses/QUARTERS/FP/Labs/CedarRope/rope-paper.pdf)
