# 04 — Medium — Vertex Load Assignment

**Task**: Assign bandwidth to every node in a network so adjacent nodes differ by at most 1, matching the fixed nodes and minimising the total.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You're provisioning a network. Adjacent nodes share a link, so their bandwidth may differ by at most 1. A few nodes have a fixed requirement; the rest are `null` and yours to set. Assign non-negative loads to the free nodes so the constraint holds everywhere and the sum is as small as possible.

The graph is undirected and connected. Constraints: `1 <= n <= 200001`, every
edge endpoint is in `0..n-1`, and `loads` has exactly `n` entries. Each entry in
`loads` is either `null` or a non-negative signed 64-bit integer. The fixed
requirements are mutually feasible.

## Input

```json
{"n": 4, "edges": [[0,1],[1,2],[2,3]], "loads": [10, null, null, null]}
```
`loads[i]` is the fixed value or `null` if free.

## Output

The assigned loads, space-separated on one line.

## Examples

**Example 1** - one fixed node on a path
```
{"n":4,"edges":[[0,1],[1,2],[2,3]],"loads":[10,null,null,null]} → 10 9 8 7
```

**Example 2** - two fixed nodes constrain the middle
```
{"n":3,"edges":[[0,1],[1,2]],"loads":[5,null,8]} → 5 7 8
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

Source: original
