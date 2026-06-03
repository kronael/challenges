# 38 — Skip List

**Task**: Implement a skip list supporting insert, delete, search, and range-count, all in expected O(log n).

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

A skip list is a sorted linked list with "express lanes": each node randomly gets
a tower of forward pointers, so a search drops down levels like a binary search
over a linked list. It is the balanced-BST result with no rotations.

The difficulty is that the balance is *probabilistic*, not structural. Correctness
must hold for any random tower assignment, and the search descends levels by a
rule you have to reason about — overshoot the target at level k, drop to level
k−1, repeat. Get the descent or the level-pointer splicing wrong and it silently
loses elements.

## Input / Output

```json
{"ops": [["insert", 3], ["search", 4], ["range_count", 2, 5], ["delete", 3]]}
```
`search` emits 1/0, `range_count lo hi` emits the count in `[lo, hi]`; insert and
delete emit nothing.

## Examples

**Example 1** — range_count drops after the delete inside the range.
```
insert 3,1,7,4; search4→1; search5→0; insert2; range_count(2,5)→3; delete3; range_count(2,5)→2
  → 1 0 3 2
```

**Example 2** — operations on an empty list, then a degenerate range.
```
search0→0; range_count(-10,10)→0; insert0; search0→1; range_count(-10,10)→1
  → 0 0 1 1
```

## Teaches

- **Probabilistic balancing**: each node's height comes from a geometric distribution (flip until tails, P=0.5), giving expected O(log n) with no rebalancing.
- **Level-descending search**: walk from the top level down, dropping a level whenever the next node would overshoot the target.

## Run

```
cd rust   && make
cd python && make
```

Source: [Pugh, *Skip Lists: A Probabilistic Alternative to Balanced Trees* (CACM 1990)](https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf)
