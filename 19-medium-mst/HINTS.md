# Hints — 19 Medium — Minimum Spanning Tree

> Spoilers. Open only when stuck.

- **Greedy by the cut property**: sort the roads cheapest-first and add each one
  that joins two different components; it is always safe to take. Unlike coin
  change, greedy is provably optimal here — an exchange argument shows the
  cheapest crossing edge of any cut belongs to some MST.
- **DSU for cycle tests**: union-find answers "would this road create a cycle?"
  in O(α) per query — far cheaper than rescanning the partial network. Each
  added edge unions the two components; an edge whose endpoints already share a
  root is the one that would close a loop, so skip it. This makes the whole
  algorithm O(m log m), dominated by the sort.

The naive approach — for each candidate edge, walk the partial tree (BFS/DFS)
to see whether its endpoints are already connected — is correct but
O(m · (n + m)). That is what `rotten/main.py` does: it matches the answer on
small cases but TIMEOUTs on the large ones.

Source: CLRS §23, minimum spanning trees
