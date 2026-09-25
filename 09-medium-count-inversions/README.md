# 09 — Medium — Count Inversions

**Task**: Count exactly how many out-of-order pairs an array has — a measure of how far it is from sorted.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

An array is "almost sorted" if it has few *inversions*: index pairs `i < j` where `arr[i] > arr[j]`. A sorted array has 0; a fully reversed array of `n` elements has the maximum, n(n−1)/2. Count the exact number for a given array.

Constraints: `n` up to 2·10⁵, values fit in a signed 32-bit integer; the count
itself can exceed that range, so use a signed 64-bit integer for it.

## Input

```json
{"n": 5, "arr": [2, 4, 1, 3, 5]}
```

## Output

A single integer: the number of inversions.

## Examples

**Example 1** — the inversions are (2,1), (4,1), (4,3)
```
{"n":5,"arr":[2,4,1,3,5]} → 3
```

**Example 2** — fully reversed: every pair is an inversion, 5·4/2 = 10
```
{"n":5,"arr":[5,4,3,2,1]} → 10
```

## Run

```
make -C rust
make -C go
make -C c
make -C python
```

Stuck? See `hints/01.md`.

Source: CLRS
