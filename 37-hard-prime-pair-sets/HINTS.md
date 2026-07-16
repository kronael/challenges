# Hints — 37 Hard — Prime Pair Sets

> Spoilers. Open only when stuck.

- **Model it as a graph**: compatibility (both concatenations prime) is a
  symmetric relation, so it's an undirected edge between two primes. A
  pairwise-compatible 5-set is exactly a 5-clique in that graph. The answer is
  the cheapest 5-clique.
- **Miller–Rabin primality**: deterministic over the 64-bit range, fast enough
  for the many concatenations considered during the search. One trial-division
  check at this input size is manageable; repeating it across the full set of
  candidate pairs is the expensive part.
- **Clique search by extension**: backtrack, adding only primes compatible with
  *every* current member; this pruning is what makes 5-cliques tractable. Cache
  pair compatibility so each concatenation is tested once.
- **Prune by sum**: keep the best sum found so far and stop extending a partial
  clique once `current_sum + smallest_possible_remaining` already meets it.

The naive method — enumerate primes, test every C(n,k) subset with trial-division
primality on each concatenation — is correct but hopelessly slow; that is what
`rotten/main.py` does, and it TIMEOUTs.

Source: [Project Euler #60](https://projecteuler.net/problem=60)
