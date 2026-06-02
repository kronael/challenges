# 20 — Matrix Exponentiation (Fibonacci)

Compute the `n`-th Fibonacci number modulo `1_000_000_007`, with `F(0) = 0`, `F(1) = 1`.

## Input / Output

```
{"n":<int>}
---
<value>      F(n) mod 1_000_000_007
```

## Examples

```
{"n":10}
→ 55

{"n":1000000000}
→ 21
```

## Key insight

`[[1,1],[1,0]]^n` has `F(n)` in its corner, so raising it by exponentiation-by-squaring (equivalently, fast doubling) gives `F(n)` in O(log n) modular multiplications.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
