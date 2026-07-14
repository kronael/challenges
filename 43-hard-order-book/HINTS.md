# Hints — 43 Hard — Order Book

> Spoilers. Open only when stuck.

- **One map per side, keyed by price level.** Keep `bids[price]` and
  `asks[price]`, where each entry is a FIFO queue of the resting quantities at
  that price plus a running total for the level. Time priority within a level
  falls out of the queue order; you never sort orders against each other.

- **Get the best price in O(log n), not O(n).** A heap of price levels per side
  (bids as a max-heap, asks as a min-heap) lets you read the best price off the
  top. Use **lazy deletion**: when the level on top of the heap has a running
  total of zero (fully filled), pop it and move on. That keeps `best_bid` /
  `best_ask` amortised cheap without scanning the whole book.

- **Matching loop.** For an incoming order, repeatedly take the best opposite
  price. Stop when the opposite side is empty, or — for a limit order — when the
  best opposite price is on the wrong side of the limit (a buy stops once the
  best ask exceeds its price; a sell stops once the best bid falls below its
  price). A market order has no such guard. At each level, drain the FIFO queue,
  taking `min(remaining_incoming, front_resting)` each step and emitting a trade
  at the resting price.

- **After matching, rest the remainder — but only for limit orders.** A limit
  order's leftover quantity rests at its own price (push the level onto the heap
  if it is new). A market order's leftover is simply dropped.

- **Output.** Count trades, emit each `price qty` pair in occurrence order, then
  the four book-state integers (best bid + its total, best ask + its total),
  reporting `0 0` for an empty side.

The naive engine in `rotten/` keeps the book as one flat list of resting orders
and, for every incoming order, linearly scans (and re-sorts) the entire list to
find the best price. It is correct, so it passes the small cases, but the
per-order O(n) scan makes it O(n²) overall and it TIMEOUTs on the large cases.
