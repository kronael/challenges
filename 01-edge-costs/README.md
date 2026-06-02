# 01 — Vertex Load Assignment

A graph (typically a tree) where vertices have integer **loads**. Some loads are missing. Any two adjacent vertices must have loads differing by **at most 1**. Assign non-negative loads to missing vertices to **minimise total load**.

## Input / Output

```
{"n":<int>,"edges":[[u,v],…],"loads":[<int|null>,…]}
---
l0 l1 … ln-1      assigned loads, space-separated
```

## Examples

```
{"n":4,"edges":[[0,1],[1,2],[2,3]],"loads":[10,null,null,null]}
→ 10 9 8 7

{"n":4,"edges":[[0,1],[0,2],[0,3]],"loads":[null,5,5,5]}
→ 4 5 5 5
```

## Run

```
cd rust   && make test
cd go     && make test
cd python && make test
```
