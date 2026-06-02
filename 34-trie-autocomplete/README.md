# 34 — Trie Autocomplete

Build a trie (prefix tree) over a dictionary of `words`. For each `query`,
return the up-to-3 lexicographically smallest words in the dictionary that
have the query as a prefix.

The dictionary is given pre-sorted, so when you walk the subtree under a
prefix node in alphabetical order, the first three leaves you reach are the
answer. A sorted-list scan would be `O(words × queries)`; the trie makes each
query cost only the prefix length plus a bounded subtree walk.

## Input

```json
{"words": ["mobile", "mouse", "moneypot", "monitor", "mousepad"],
 "queries": ["m", "mo", "mou", "mous", "mouse"]}
```

`1 ≤ words.length ≤ 1000`, word length `≤ 20`, `queries.length ≤ 100`.
Words are distinct, lowercase `a–z`, and given in ascending order.

## Output

One line. Query results are joined by `;`; within a result the matching words
(up to 3) are joined by a single space. A query with no match contributes an
empty segment.

```
mobile moneypot monitor;mobile moneypot monitor;mouse mousepad;mouse mousepad;mouse mousepad
```

## Example

```
{"words":["a","ab","abc"],"queries":["a","ab","abc","abcd","x"]}
→ a ab abc;ab abc;abc;;
```

## Key insight

Insert every word into the trie. To answer a query, walk down to the prefix
node (`O(len)`); if it exists, DFS its subtree visiting children in `a–z`
order and stop after collecting 3 words. Because the alphabetical DFS yields
words in sorted order, the first three are the lexicographically smallest.

Source: [LeetCode 1268 — Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/)

## Run

```
cd rust   && make test && make bench
cd go     && make test && make bench
cd python && make test && make bench
```

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.
