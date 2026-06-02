# 12 — Count Inversions

Count the inversions in an array: the number of index pairs `i < j` with `arr[i] > arr[j]`.

## Input / Output

```
{"n":<int>,"arr":[<int>,…]}
---
<count>      number of inversions
```

## Examples

```
{"n":5,"arr":[2,4,1,3,5]}
→ 3

{"n":4,"arr":[4,3,2,1]}
→ 6
```

## Key insight

Merge sort: while merging two sorted halves, each time a right-half element is taken before remaining left-half elements, those are all inversions. Counting during the merge gives O(n log n) versus the naive O(n²).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
