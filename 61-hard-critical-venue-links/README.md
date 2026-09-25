# 61 — Hard — Critical Venue Links

**Task**: Report every link in a venue network whose loss would cut the network
apart.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

An order-routing network has `n` venues numbered `0 .. n-1` joined by `m` two-way
links. `links[i] = [u, v]` is a link that carries orders in both directions
between venue `u` and venue `v`.

Two venues are **in touch** when orders can travel from one to the other along
some sequence of links. Link `i` is **critical** when taking that one link out of
service leaves at least one pair of venues that were in touch no longer in touch.

Report the position in `links` of every critical link.

Two venues may be joined by more than one link. Each such link is its own entry
of `links` with its own position, and taking one of them out of service leaves the
others carrying orders. The network need not be in one piece either: venues that
are already out of touch stay out of touch, and no link is critical on their
account.

## Constraints

- `1 <= n <= 200000`
- `0 <= m <= 300000`, and `m` equals the number of entries in `links`
- every entry is a pair of **distinct** venue numbers in `0 .. n-1`
- the same pair of venues may appear in several entries, in either order
- a venue may have no links at all
- the network is not necessarily connected

## Input

```json
{"n": 6, "links": [[0,1],[1,2],[2,0],[1,3],[3,4],[4,5]]}
```

- `n` — number of venues
- `links` — the two-way links; an entry's position in this list is its number

## Output

The positions of the critical links, in increasing order, space-separated on one
line. Print an empty line when no link is critical.

## Examples

**Example 1** — taking out position 3 leaves venues 3, 4 and 5 unable to reach
venue 0; taking out position 0, 1 or 2 leaves every pair still in touch
```
{"n":6,"links":[[0,1],[1,2],[2,0],[1,3],[3,4],[4,5]]} → 3 4 5
```

**Example 2** — taking out any one of these four links still leaves all four
venues in touch, so the answer line is empty
```
{"n":4,"links":[[0,1],[1,2],[2,3],[3,0]]} → (empty line)
```

**Example 3** — positions 0 and 1 both join venues 0 and 1, so taking out either
one leaves the other carrying orders; position 2 is the only link at venue 2
```
{"n":3,"links":[[0,1],[1,0],[1,2]]} → 2
```

**Example 4** — venues 7 and 8 have no links, and venues 4, 5 and 6 are out of
touch with the rest from the start
```
{"n":9,"links":[[0,1],[1,2],[2,0],[2,3],[4,5],[5,6]]} → 3 4 5
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
