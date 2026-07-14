# 36 — Hard — Matrix Chain Multiplication

**Task**: Find the parenthesization of a matrix product that minimises scalar multiplications.

**Difficulty**: hard
**Time estimate**: ~50 min

## Problem

You need to multiply a chain of `k` matrices, `A₁ · A₂ · … · A_k`, where matrix
`i` has dimensions `dims[i-1] × dims[i]`. Matrix multiplication is associative —
the final product is the same no matter how you parenthesize it — but the *cost*
is not. Multiplying a `p×q` matrix by a `q×r` matrix takes `p·q·r` scalar
multiplications, so the order in which you pair up the matrices decides the total
work, and a good order versus a bad one can differ by orders of magnitude.

Given the dimension list, output the minimum number of scalar multiplications
needed to compute the whole product.

Constraints: `k` up to 500 matrices (so up to 501 dimensions), each dimension up
to 100.

## Input

```json
{"dims": [10, 30, 5, 60]}
```

`k+1` dimensions for `k` matrices; matrix `i` is `dims[i] × dims[i+1]`.

## Output

A single integer: the minimum number of scalar multiplications.

## Examples

**Example 1** — the two orders differ hugely
```
dims [10,30,5,60] → 4500   (A·B)·C costs 4500 vs A·(B·C) at 27000
```

**Example 2** — two matrices, only one order
```
dims [5,10,20] → 1000
```

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.
