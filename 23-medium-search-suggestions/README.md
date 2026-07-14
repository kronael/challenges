# 23 — Medium — Search Suggestions

**Task**: For each search query, return the up to 3 lexicographically smallest words in a sorted dictionary that have the query as a prefix.

**Difficulty**: medium
**Time estimate**: ~45 min

## Problem

Given a pre-sorted word list and a stream of queries, emit the up to three
lexicographically smallest words that have the query as a prefix — exactly what a
search box shows as you type. An empty query matches every word, so it returns the
three smallest words overall; a query with no matching word returns nothing.

Constraints: up to 5·10⁴ words and 5·10³ queries; words are lowercase `a`–`z`,
each up to 20 characters; the word list arrives already sorted.

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

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: [LeetCode 1268 — Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/)
