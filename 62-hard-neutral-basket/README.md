# 62 — Hard — Neutral Basket

**Task**: Choose which of a desk's positions go into one basket so the basket's
net exposure lands as close as possible to a mandated figure.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

A desk holds `n` positions. `exposures[i]` is the signed exposure of position
`i`: positive for a long, negative for a short, and all of them quoted in the
same currency, so exposures add.

You choose which positions go into one basket. The basket's **net exposure** is
the total of the exposures of the positions you put in it. Risk has mandated that
the basket net `target` — a `target` of 0 asks for a basket that is exactly flat,
and any other `target` for a basket carrying exactly that much one-way exposure.
The mandate is rarely reachable to the penny.

Report the smallest distance `|net exposure - target|` that any choice of
positions achieves.

Every choice of positions is allowed, the two extremes included: the **empty
basket**, which nets 0, and the basket holding **all `n` positions**. Positions
are chosen one by one and not by size, so two positions that happen to carry the
same exposure are still two separate positions, and either, neither, or both may
go in.

## Constraints

- `1 <= n <= 38`, and `n` equals the number of entries in `exposures`
- `-10^12 <= exposures[i] <= 10^12`; an exposure may be positive, negative, or 0
- `-10^13 <= target <= 10^13`
- exposures may repeat, and `target` may be exactly reachable, unreachable, or
  outside the range of anything the desk can net
- every net exposure and the reported distance fit in a signed 64-bit integer

## Input

```json
{"n": 5, "target": -3, "exposures": [4, -7, 2, 9, -1]}
```

- `n` — number of positions on the desk
- `target` — the net exposure the basket is mandated to carry
- `exposures` — the signed exposure of each position

## Output

A single integer: the smallest distance any basket's net exposure achieves
from `target`.

## Examples

**Example 1** — positions 0 and 1 net `4 + (-7) = -3`, the mandate exactly
```
{"n":5,"target":-3,"exposures":[4,-7,2,9,-1]} → 0
```

**Example 2** — every exposure here is even and the mandate is odd, so no basket
nets it; positions 1 and 3 net -30, one away
```
{"n":6,"target":-31,"exposures":[-4,-10,-14,-20,-6,-12]} → 1
```

**Example 3** — every position carries the wrong sign for this mandate, so the
empty basket, at 0, is the closest any basket gets
```
{"n":5,"target":-1000,"exposures":[3,17,42,8,25]} → 1000
```

**Example 4** — the whole desk nets `10+20+30+40 = 100`, short of the mandate, so
the basket holding all four positions is the closest
```
{"n":4,"target":250,"exposures":[10,20,30,40]} → 150
```

## Run

```
make -C rust
make -C go
make -C c
make -C python
```

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.

Stuck? See `hints/01.md`.
