# 14 — Union-Find

**Task**: Maintain friend groups as friendships form, and answer whether two people are connected.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You're building a social network. As friendships form, you need to instantly answer: are these two people already in the same friend group? Support N people, M friend connections, and K queries — the merges arrive in arbitrary order, so you can't pre-sort. The non-trivial part: keep every operation near-constant no matter how the groups grow.

## Input

```json
{"n": 5, "unions": [[0,1],[1,2],[3,4]], "queries": [[0,2],[0,3],[3,4]]}
```

## Output

One value per query on a single line: `1` if the pair shares a component, else `0`.

## Examples

**Example 1** — connectivity is transitive across a chain of merges
```
n=5, unions [0,1][1,2][3,4], queries [0,2][0,3][3,4] → 1 0 1
```

**Example 2** — separate components stay separate
```
n=3, unions [], queries [0,1] → 0
```

## Teaches

- **Disjoint-set union**: connectivity reduces to "same root", turning a relation into pointer chasing.
- **Two tricks together**: path compression plus union by rank give inverse-Ackermann (effectively constant) per op — neither alone is enough.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: CLRS §21
