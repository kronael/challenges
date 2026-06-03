# 20 — Matrix Exponentiation

**Task**: Compute the Nth Fibonacci number mod 10^9+7, where N can be 10^9.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Compute `F(n) mod 1e9+7` for `n` up to 10^9. Iterating the recurrence is O(n) — far too slow at this scale. The insight: a linear recurrence is a matrix multiplication, and `[[1,1],[1,0]]^n` carries `F(n)` in a corner. Raising that matrix to a power can be done by squaring in O(log n) steps.

## Input

```json
{"n": 10}
```

## Output

A single integer: `F(n) mod 1_000_000_007`.

## Examples

**Example 1** — small case
```
n=10 → 55
```

**Example 2** — n far beyond what O(n) iteration could reach
```
n=1000000000 → 21
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
