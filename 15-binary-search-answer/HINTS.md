# Hints — 15 Binary Search on the Answer

> Spoilers. Open only when stuck.

- **Optimization → decision**: rewrite "find the minimum feasible X" as "is X
  feasible?". For a fixed cap on the largest block, "can this be done with at most K
  students?" is a monotone predicate — once a cap works, every larger cap works too.
- **Binary-search the answer, not the array**: the smallest workable cap lives in
  `[max(pages), sum(pages)]`. Binary-search that range; each probe asks the decision
  question, so the whole thing is O(n log sum) instead of exponential.
- **Greedy feasibility check**: walk the books left to right, greedily filling the
  current student until the next book would exceed the cap, then start a new student.
  Counting the students this needs is one O(n) pass per probe.

The naive approach — enumerate every way to cut the row into blocks (or an
exponential recursion over split points) — is what `rotten/main.py` does: correct,
but it TIMEOUTs on the large cases.
