# Hints — 12 Count Inversions

> Spoilers. Open only when stuck.

- **Count during the merge**: run a merge sort. Every time you pull an element
  from the right half ahead of `k` elements still waiting in the left half,
  those `k` pairs are inversions — add `k` to the total. The counting rides
  along for free.
- **Divide and conquer**: total = left inversions + right inversions + cross
  inversions, all computed inside one merge-sort recursion in O(n log n).
- **Use i64**: the count can exceed i32 (a fully reversed array of `n` elements
  has n(n−1)/2 inversions, which overflows 32 bits well before n = 10⁵).

The naive O(n²) double loop (`for i: for j>i: if arr[i] > arr[j]: count += 1`)
is what `rotten/main.py` does — correct, but it TIMEOUTs on the large cases.
