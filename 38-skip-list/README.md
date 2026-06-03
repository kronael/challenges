# 38 — Skip List

Probabilistic ordered set supporting insert, delete, search, and `range_count`, all expected O(log n).
Hard because the balance is *probabilistic*, not structural — there are no rotations, so correctness must hold for any random tower of levels, and the level-descending walk has to be reasoned about, not memorised.

## Input / Output
```
{"ops":[["insert",v] | ["delete",v] | ["search",v] | ["range_count",lo,hi], …]}
---
r0 r1 …    search emits 1/0, range_count emits the count; insert/delete emit nothing
```

## Teaches

- **Probabilistic balancing**: each node's height comes from a geometric distribution (flip until tails, P=0.5), giving expected O(log n) for all operations with no rebalancing.
- **Level-descending search**: walk from the top level down, dropping a level whenever the next node would overshoot the target.

## Run
```
cd rust   && make
cd python && make
```
Source: [Pugh, *Skip Lists: A Probabilistic Alternative to Balanced Trees* (CACM 1990)](https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf)
