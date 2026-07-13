# 41 — Order Book

**Task**: Replay a stream of buy/sell orders through a matching engine and report the trades it produces and the state of the book left behind.

**Difficulty**: medium
**Time estimate**: ~45 min

## Problem

You are given a chronological stream of orders arriving at an exchange. Each
order has a `side` (`"buy"` or `"sell"`), a `type` (`"limit"` or `"market"`), a
`price`, and a quantity `qty`. Process the orders one at a time, in the order
given, against a single instrument's book.

The book holds *resting* orders that have not yet traded — bids (resting buys)
on one side, asks (resting sells) on the other. When a new order arrives it is
matched against the opposite side under **price-time priority**:

- A buy matches against the lowest-priced asks first; a sell matches against the
  highest-priced bids first. The best price always trades first.
- Among resting orders at the *same* price, the one that arrived earliest trades
  first (first in, first out).

A **trade** happens whenever an incoming order takes quantity from a resting
order. The trade's price is the resting order's price, and its quantity is
however much was taken (the smaller of what the incoming order still wants and
what that resting order has left). A single incoming order can produce several
trades as it walks across multiple resting orders and price levels.

The two order types differ only in how far they are willing to match:

- A **limit** order names a worst acceptable price. A buy limit at `price` will
  only take asks priced `≤ price`; a sell limit at `price` will only take bids
  priced `≥ price`. Whatever quantity is left unmatched **rests** in the book at
  its limit price, becoming available to later orders.
- A **market** order has no price guard — it matches against the best available
  prices until either it is filled or the opposite side is empty. Any unmatched
  remainder is **discarded**, never rested. (Its `price` field is ignored; cases
  use `0`.)

Constraints: up to `2·10⁵` orders; prices and quantities are positive integers
fitting in i32 (a market order's price may be `0`).

## Input

```json
{"orders": [
  {"side": "sell", "price": 100, "qty": 5, "type": "limit"},
  {"side": "buy",  "price": 105, "qty": 8, "type": "limit"}
]}
```

## Output

A single line of space-separated integers:

```
T  p1 q1  p2 q2  ...  pT qT  best_bid bid_qty best_ask ask_qty
```

- `T` — the number of trades produced.
- Then `T` pairs `pi qi`, in the order the trades occurred: price and quantity
  of each trade.
- Then four trailing integers describing the final book: the best (highest) bid
  price and the total quantity resting at it, then the best (lowest) ask price
  and the total quantity resting at it. A side that is empty reports `0 0`.

## Examples

**Example 1** — empty stream: no trades, empty book
```
{"orders":[]} → 0 0 0 0 0
```

**Example 2** — a buy that crosses a resting sell, leaving the remainder on the bid
```
{"orders":[{"side":"sell","price":100,"qty":5,"type":"limit"},{"side":"buy","price":105,"qty":8,"type":"limit"}]} → 1 100 5 105 3 0 0
```
The buy takes all 5 at the ask price 100 (one trade), then its remaining 3 rest
as a bid at 105. Final book: best bid `105 3`, no asks `0 0`.

**Example 3** — a market buy sweeps two ask levels, then is exhausted
```
{"orders":[{"side":"sell","price":101,"qty":3,"type":"limit"},{"side":"sell","price":103,"qty":4,"type":"limit"},{"side":"buy","price":0,"qty":6,"type":"market"}]} → 2 101 3 103 3 0 0 103 1
```
The market buy takes 3 at 101, then 3 of the 4 at 103 (two trades), filling its
6. One unit remains resting at ask 103. Final book: no bids `0 0`, best ask `103 1`.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: limit order book / price-time priority matching (continuous double auction)
