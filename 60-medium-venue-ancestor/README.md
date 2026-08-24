# 60 — Medium — Venue Ancestor

**Task**: For each pair of venues, report the deepest venue that both of their
order routes pass through.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

An order-routing hierarchy holds `n` venues numbered `0 .. n-1`. Every venue
forwards whatever it cannot fill to exactly one parent venue. `parent[i]` is the
venue that `i` forwards to, and `parent[r]` is `-1` for the single root venue
`r`, which forwards nowhere.

An order placed at venue `v` is routed through `v`, then `parent[v]`, then that
venue's parent, and so on until it reaches the root. Call that sequence the
**route** of `v`.

For each pair `(a, b)` in the batch, report the **deepest venue on both routes**:
the venue furthest from the root that the route of `a` and the route of `b` both
contain. A venue is on its own route, so the answer for `(a, a)` is `a`, and if
the route of `b` contains `a` then the answer is `a`.

Answer every pair in the batch, in the order the pairs are given.

## Constraints

- `1 <= n <= 200000`, and `parent` has exactly `n` entries
- exactly one entry of `parent` is `-1`; the root is not necessarily venue `0`
- a parent's number may be smaller or larger than the venue's own number
- following parents from any venue reaches the root: the hierarchy is a tree
- `1 <= q <= 5000`, and `q` equals the number of pairs
- both entries of a pair are venue numbers in `0 .. n-1`, and they may be equal

## Input

```json
{"n": 7, "parent": [-1, 0, 0, 1, 1, 2, 2], "queries": [[3, 4], [3, 5], [1, 3]]}
```

- `n` — number of venues
- `parent` — `parent[i]` is the venue that `i` forwards to, `-1` for the root
- `queries` — the pairs to answer, in order

## Output

The answer for each pair, in the order given, space-separated on one line.
Exactly `q` venue numbers.

## Examples

**Example 1** — venues 3 and 4 both forward to venue 1; venues 3 and 5 share
only the root; venue 1 is on the route of venue 3
```
{"n":7,"parent":[-1,0,0,1,1,2,2],"queries":[[3,4],[3,5],[1,3]]} → 1 0 1
```

**Example 2** — a hierarchy that is one long line
```
{"n":4,"parent":[-1,0,1,2],"queries":[[3,1],[2,2],[0,3]]} → 1 2 0
```

**Example 3** — the root is venue 1 here, and venue 0 is a leaf
```
{"n":3,"parent":[1,-1,1],"queries":[[0,1],[0,2]]} → 1 1
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
