# Hints — 11 Interval Scheduling

> Spoilers. Open only when stuck.

- **Earliest-finish-time greedy**: sort the meetings by end time, then sweep
  left to right taking each meeting whose start `≥` the last accepted end.
  Finishing each meeting as soon as possible leaves the most room for the rest.
- **Why earliest *end*, not earliest *start* or shortest**: earliest-start lets
  one long meeting hog the morning; shortest-first can split a pair that would
  have fit. Only the earliest-end key is provably optimal.
- **Exchange argument**: any optimal schedule can be rewritten to start with the
  earliest-finishing pick without losing meetings — that is the proof of
  optimality.

The naive approach tries every subset of meetings, or every starting choice via
recursion, and keeps the largest non-overlapping one. It is correct but
exponential, so it TIMEOUTs on the large cases. That is what `rotten/main.py`
does.

Source: CLRS §16.1
