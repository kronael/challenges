# Hints — 29 Distinct Substrings

> Spoilers. Open only when stuck.

- **Every substring is a prefix of exactly one suffix.** So if you sort all `n`
  suffixes, you can count distinct substrings by walking the sorted list once and
  subtracting away the prefixes shared between adjacent suffixes.
- **Suffix array (O(n log n))**: sort all suffixes by prefix doubling — sort by
  the first character, then first 2, 4, 8, … characters, reusing ranks each round.
- **Kasai's LCP**: the longest common prefix of adjacent sorted suffixes, computed
  in O(n) by reusing the previous LCP value (it drops by at most one per step).
- **The formula**: total prefixes `n(n+1)/2` minus `Σ LCP` removes exactly the
  double-counted shared prefixes, leaving the count of distinct substrings.

The naive approach (dump every substring into a hash set) is correct but is what
`rotten/main.py` does — it TIMEOUTs and blows up memory on the large cases.
