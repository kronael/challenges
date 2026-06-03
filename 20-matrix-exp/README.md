# 20 — Matrix Exponentiation (Fibonacci)

Compute `F(n) mod 1e9+7` for `n` up to a billion. The challenge is collapsing a linear recurrence into a logarithmic number of steps.

## Input / Output

```
{"n":<int>}
---
<value>      F(n) mod 1_000_000_007
```

## Example

```
{"n":10}
→ 55
```

## Teaches

- **Recurrence as matrix power**: `[[1,1],[1,0]]^n` holds `F(n)` in a corner; any linear recurrence becomes a matrix raised to a power.
- **O(log n) via squaring**: exponentiation-by-squaring on the transition matrix (equivalently fast doubling) turns an O(n) scan into O(log n) multiplies.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: competitive classic
