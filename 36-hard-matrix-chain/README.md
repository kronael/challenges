# 36 — Hard — Matrix Chain Multiplication

**Task**: Find the minimum number of scalar multiplications needed for a matrix
chain product.

**Difficulty**: hard
**Time estimate**: ~50 min

## Problem

You need to multiply a chain of `k` matrices, `A₀ · A₁ · … · Aₖ₋₁`, where
zero-based matrix `i` has dimensions `dims[i] × dims[i+1]`. Matrix
multiplication is associative —
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

The list contains `k+1` dimensions for `k` matrices. Matrix indices start at
zero, so matrix `i` is `dims[i] × dims[i+1]`.

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
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
