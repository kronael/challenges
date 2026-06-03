# 34 — Trie Autocomplete

**Task**: For each search query, return the up to 3 lexicographically smallest words in a sorted dictionary that have the query as a prefix.

**Difficulty**: medium
**Time estimate**: ~45 min

## Problem

Given a pre-sorted word list and a stream of queries, emit the three smallest
matches for each prefix — exactly what a search box shows as you type. The
brute-force scan is O(k · |words|): for every query you re-scan the whole list.

Build the trie once in O(|words|). A query then walks to the prefix node in
O(|query|), and an alphabetical DFS of that subtree yields words already sorted —
take the first three and stop. No per-query scan, no per-query sort.

## Input / Output

```json
{"words": ["mobile", "moneypot", "monitor", "mouse", "mousepad"], "queries": ["m", "mo", "mou", "mous", "mouse"]}
```
One output line; query results joined by `;`, up to 3 words per result joined by
` `, an empty segment when nothing matches.

## Examples

**Example 1** — first three in alphabetical order, capped at 3.
```
queries ["m","mo","mou","mous","mouse"]
  → mobile moneypot monitor;mobile moneypot monitor;mouse mousepad;mouse mousepad;mouse mousepad
```

**Example 2** — catches missing empty-segment handling on no match.
```
words ["a","ab","abc"], queries ["a","ab","abc","abcd","x"]
  → a ab abc;ab abc;abc;;
```

## Teaches

- **Trie (prefix tree)**: 26-ary nodes; reaching the prefix costs O(len), independent of dictionary size.
- **DFS for lexicographic order**: visiting children a–z and stopping after 3 leaves gives the smallest matches with no re-sorting.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: [LeetCode 1268 — Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/)
