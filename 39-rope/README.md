# 39 — Rope

A **rope** is a binary tree of string fragments. Leaves hold contiguous text;
each internal node stores its left subtree's total length (its *weight*) so the
tree can be indexed in `O(log n)` without ever materialising the whole string.
Concatenation is `O(1)` — just hang two ropes off a new root.

Build a rope from a list of `parts` (concatenated in order), then answer
substring queries `[lo, hi)` (half-open, like Python slicing).

The point: a naive `s += part` loop is `O(total²)` because each `+` copies the
prefix again. A rope builds in `O(n log n)` and slices in `O(log n + k)`.

## Input / Output

```
{"parts":["abc","def",…],"queries":[[lo,hi],…]}
---
sub0|sub1|…      extracted substrings, joined by '|'
```

Each query is clamped to `[0, total_len)`; an empty range yields an empty
piece. Parts and substrings never contain `|` or whitespace.

## Examples

```
{"parts":["abc","def","ghi","jkl"],"queries":[[0,5],[3,9],[6,12]]}
→ abcde|defghi|ghijkl
```

Concatenated text is `abcdefghijkl`. `[0,5)="abcde"`, `[3,9)="defghi"`,
`[6,12)="ghijkl"`.

```
{"parts":["hello","world","foo"],"queries":[[0,8],[5,5],[2,6]]}
→ hellowor||llow
```

Text is `helloworldfoo`. `[0,8)="hellowor"`, `[5,5)=""` (empty), `[2,6)="llow"`.

## Constraints

- total length of all parts up to `10⁶`
- up to `10⁴` parts, up to `10⁴` queries
- ASCII text

Large case: 1000 parts of ~100 chars each (~100k total), 10k queries.

## Notes

Build the tree bottom-up by pairwise merging (balanced, depth `O(log n)`) — a
naive left fold makes a right-leaning chain that degrades indexing to `O(n)`.
`extract(lo, hi)` walks down comparing the cut points against each node's
weight, descending left when `lo < weight` and right when `hi > weight`
(subtracting the weight on the way right). Do **not** use a `Rope` library —
write the tree yourself.

Source: https://en.wikipedia.org/wiki/Rope_(data_structure) ·
https://www.geeksforgeeks.org/dsa/ropes-data-structure-fast-string-concatenation/

## Run

```
cd rust   && make test && make bench
cd python && make test && make bench
```

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.
