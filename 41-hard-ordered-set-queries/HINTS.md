# Hints — 41 Hard — Skip List

> Spoilers. Open only when stuck.

- **Express lanes**: a skip list is a sorted linked list where each node randomly
  gets a *tower* of forward pointers. Higher levels skip over many nodes at once,
  so a search drops down levels like a binary search over a linked list. It is the
  balanced-BST result with no rotations.
- **Probabilistic balancing**: each node's height comes from a geometric
  distribution (flip a coin until tails, `P = 0.5`), capped at some `MAX_LEVEL`.
  That alone gives expected O(log n) per operation with no rebalancing — the
  balance is statistical, not maintained by any explicit invariant.
- **Level-descending search**: start at the head on the topmost level. While the
  next node would *not* overshoot the target (`next.val < target`), step forward;
  otherwise drop down one level and repeat. At level 0 the node after where you
  stop is the candidate. Overshoot the target at level k, drop to level k−1,
  repeat.
- **The `update` array**: for insert and delete, record, at every level, the last
  node you stopped on before dropping. Those are exactly the predecessors whose
  forward pointers must be spliced when wiring in (or unlinking) the target node.
  Get this splicing wrong at any single level and the structure silently loses
  elements.
- **range_count(lo, hi)**: descend to the first node with `val >= lo`, then count
  nodes until `val > hi`. Carrying a width/span per forward pointer lets you
  compute ranks and answer the count as `rank(hi) - rank(lo - 1)` in expected
  O(log n); without spans, this step is output-sensitive.

The naive approach — keep a plain sorted list (or rescan a linked list) and do an
O(n) insert/search/count per op — is correct but O(n) per operation, so it
TIMEOUTs on the large cases. That is what `rotten/main.py` does.

Source: [Pugh, CACM 1990](https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf)
