# 12 — Count Inversions

Count the inversions in an array: index pairs `i < j` with `arr[i] > arr[j]`. The interesting part is counting them as a side effect of merge sort, dropping the naive O(n²) to O(n log n).

**Difficulty: medium** — one divide-and-conquer with a counting twist, solvable in ~30 min.

## Input / Output

```
{"n":<int>,"arr":[<int>,…]}
---
<count>      number of inversions
```

## Example

```
{"n":5,"arr":[2,4,1,3,5]}
→ 3      (2,1),(4,1),(4,3)
```

## Teaches

- **Counting during the merge**: when a right-half element is emitted ahead of `k` remaining left-half elements, those `k` form inversions; summing them counts all cross-half pairs.
- **Divide and conquer**: total = left inversions + right inversions + cross inversions, each computed within the same merge-sort recursion.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS
