# 55 — Hard — Changing Network Queries

**Task**: Answer connectivity queries while links are repeatedly added and
removed.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

An undirected network has `n` vertices numbered `0` through `n-1`. Process a
sequence of operations:

- `add u v` activates an inactive edge.
- `remove u v` removes an active edge.
- `ask u v` asks whether the two vertices are connected through active edges.

The full operation sequence is available before processing begins. Every
removal has a matching earlier addition, and an edge is never added twice while
active.

Constraints: `1 <= n <= 200000` and at most `200000` operations.

## Input

```json
{"n":4,"operations":[{"type":"add","u":0,"v":1},{"type":"ask","u":0,"v":2},{"type":"add","u":1,"v":2},{"type":"ask","u":0,"v":2}]}
```

## Output

Print one `0` or `1` for each `ask`, in input order, separated by spaces.

## Example

```text
0 1
```

## Run

```bash
make -C python
make -C go
make -C rust
```

Stuck? See `HINTS.md`.
