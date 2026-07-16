# 52 — Hard — Service Pairing

Assign every service to a different host while minimizing total cost.

`costs[i][j]` is the cost of placing service `i` on host `j`. There are equally
many services and hosts. A valid placement uses every row and every column
exactly once.

## Input

```json
{"costs":[[9,2,7],[6,4,3],[5,8,1]]}
```

Constraints: `1 ≤ n ≤ 500`; the matrix is `n × n`; every cost is a signed
32-bit integer; the minimum total fits in a signed 64-bit integer.

## Output

Print the minimum total cost.

## Example

```text
{"costs":[[9,2,7],[6,4,3],[5,8,1]]} → 9
```

## Run

```text
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
