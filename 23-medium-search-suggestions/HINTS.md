# Hints — 23 Medium — Trie Autocomplete

> Spoilers. Open only when stuck.

- **Trie (prefix tree)**: build it once in time proportional to the total number
  of input characters, with one node per character and 26 possible children
  (`a`–`z`). Reaching the node for a query then costs O(|query|), independent of
  how many words are in the dictionary — that is what kills the per-query
  re-scan.
- **Walk to the prefix node, then explore its subtree**: a query first walks down
  the trie character by character; if any character is missing the query has no
  matches and you emit the empty segment. Otherwise every word in the subtree
  rooted at that node has the query as a prefix.
- **DFS for lexicographic order**: visiting children in `a`–`z` order during a
  depth-first walk yields the matching words already sorted, so you can stop after
  collecting three — no per-query sort, no scanning the rest of the subtree.
- **Empty query**: it walks zero steps and lands on the root, so its subtree is the
  whole dictionary; the same DFS returns the three smallest words overall.

### Alternative: precompute the prefix answers

Because the dictionary already arrives in lexicographic order, you can build a
hash map from each prefix to its first three words. Visit the words in input
order, enumerate every prefix of each word (including the empty prefix), and add
the word only while that prefix has fewer than three stored suggestions. Each
query then becomes a direct lookup. At most 20 prefixes are visited per word;
with ordinary substring hashing this can inspect O(|word|²) characters per word,
but the stated 20-character cap keeps that bounded. Store at most three word
references per distinct prefix.

The naive O(queries · |words|) approach (for each query, scan all words, keep the
prefix matches, sort them, take three) is what `rotten/main.py` does — correct, but
it TIMEOUTs on the large cases.
