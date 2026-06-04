# 12 — Count Inversions

**Task**: Count exactly how many out-of-order pairs an array has — a measure of how far it is from sorted.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

An array is "almost sorted" if it has few *inversions*: index pairs `i < j` where `arr[i] > arr[j]`. A sorted array has 0; a fully reversed array of `n` elements has the maximum, n(n−1)/2. Count the exact number for a given array.

Checking every pair is O(n²) — fine for n=1000, hopeless at n=10⁵ (that's 5 billion comparisons). The count alone must come back fast, so the all-pairs scan is the trap to avoid.

Constraints: n up to 10⁵, values fit in i32; the count can exceed i32 — use i64.

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
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: CLRS
