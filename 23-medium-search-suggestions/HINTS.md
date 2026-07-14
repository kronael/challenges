# Hints — 23 Medium — Trie Autocomplete

> Spoilers. Open only when stuck.

- **Trie (prefix tree)**: build it once over the whole dictionary in O(|words|),
  with one node per character and 26 possible children (`a`–`z`). Reaching the node
  for a query then costs O(|query|), independent of how many words are in the
  dictionary — that is what kills the per-query re-scan.
- **Walk to the prefix node, then explore its subtree**: a query first walks down
  the trie character by character; if any character is missing the query has no
  matches and you emit the empty segment. Otherwise every word in the subtree
  rooted at that node has the query as a prefix.
- **DFS for lexicographic order**: visiting children in `a`–`z` order during a
  depth-first walk yields the matching words already sorted, so you can stop after
  collecting three — no per-query sort, no scanning the rest of the subtree.
- **Empty query**: it walks zero steps and lands on the root, so its subtree is the
  whole dictionary; the same DFS returns the three smallest words overall.

The naive O(queries · |words|) approach (for each query, scan all words, keep the
prefix matches, sort them, take three) is what `rotten/main.py` does — correct, but
it TIMEOUTs on the large cases.
