# Hints — 56 Hard — Orthogonal Segment Crossings

> Spoilers. Open only when stuck.

- Sweep from left to right. A horizontal segment becomes active at `x1` and
  stops being active after `x2`.
- At a vertical segment's x-coordinate, count active horizontal y-values in
  `[y1, y2]`.
- Coordinate-compress horizontal y-values and maintain active multiplicities in
  a Fenwick tree. Two prefix sums answer each vertical range query.
- Event ordering handles closed endpoints: add horizontals first, query
  verticals second, and remove horizontals last at the same x-coordinate.
- Testing every horizontal against every vertical is correct but takes `H*V`
  work. That direct double loop is the rotten reference.

Source: [Bentley and Ottmann — Algorithms for reporting and counting geometric intersections](https://doi.org/10.1109/TC.1979.1675432)
