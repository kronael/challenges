# 34 — Trie Autocomplete

Build a trie over a pre-sorted dictionary; for each query return the 3 lexicographically smallest words having the query as a prefix.
Medium because the insight is that an alphabetical DFS of the prefix subtree yields words already sorted, so the first three leaves are the answer — no separate sort, no scanning all words per query.

## Input / Output
```
{"words":[…sorted, lowercase…], "queries":[…]}
---
one line; query results joined by ';', up to 3 words per result joined by ' ', empty segment on no match
```

## Teaches

- **Trie (prefix tree)**: 26-ary nodes; walking to the prefix node costs O(len), independent of dictionary size.
- **DFS for lexicographic order**: visiting children a–z and stopping after 3 words gives the smallest matches without re-sorting.

## Run
```
cd rust   && make
cd go     && make
cd python && make
```
Source: [LeetCode 1268 — Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/)
