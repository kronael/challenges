# 11 — Medium — Friend Groups

**Task**: Maintain friend groups as friendships form, and answer whether two people are connected.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You're building a social network. As friendships form, you need to instantly
answer: are these two people already in the same friend group? Connectivity is
transitive — if A is friended to B and B to C, then A and C are in the same
group even with no direct link.

You are given `n` people, numbered `0..n-1`, a list of friendships to apply in
order, then a list of pairs to test. For each test pair, report whether the two
people end in the same group.

Constraints: `1 <= n <= 200000`, with at most 200000 friendships and 200000
queries. Every person ID is in `0..n-1`. Self-friendships, repeated
friendships, and repeated queries are valid. A query may also contain the same
person twice.

## Input

```json
{"n": 5, "unions": [[0,1],[1,2],[3,4]], "queries": [[0,2],[0,3],[3,4]]}
```

## Output

One value per query on a single line: `1` if the pair shares a component, else `0`.

## Examples

**Example 1** — connectivity is transitive across a chain of friendships
```
n=5, unions [0,1][1,2][3,4], queries [0,2][0,3][3,4] → 1 0 1
```

**Example 2** — separate components stay separate
```
n=3, unions [], queries [0,1] → 0
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
