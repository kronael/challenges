# Hints — 18 Count Primes

> Spoilers. Open only when stuck.

- **Mark composites instead of testing primes**: rather than asking "is this
  number prime?" for each candidate, strike out the multiples of every prime you
  find, so each composite gets marked rather than tested.
- **Sieve of Eratosthenes**: mark composites by striking multiples of each prime
  starting at `p²`; total work is O(n log log n), far below per-number testing.
- **Cache- and memory-aware sieving**: an odd-only bytearray halves space, and
  for very large `n` a segmented sieve keeps the working set in cache.

The naive O(n√n) trial-division approach (test each candidate against divisors up
to its square root) is what `rotten/main.py` does — correct but it TIMEOUTs on
the large cases.
