# 19 — Fast Modular Exponentiation

**Task**: Compute `(base^exp) mod m` where `exp` can be up to 10^18.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Given three integers `base`, `exp`, and `mod`, compute `(base^exp) mod m`.

The exponent is the catch: it can be as large as 10^18. Multiplying `base` by
itself `exp` times would take 10^18 steps — it will never finish. And even the
intermediate products are dangerous: `base^exp` is an astronomically large
number, so any value you carry between steps must stay bounded or it overflows a
64-bit word long before you reach the answer.

Constraints: `0 ≤ base, exp ≤ 10^18`, `1 ≤ mod ≤ 10^18`.

## Input

```json
{"base": 3, "exp": 5, "mod": 7}
```

## Output

A single integer: `(base^exp) mod m`.

## Examples

**Example 1** — small case to anchor the idea
```
base=3, exp=5, mod=7 → 5   (243 mod 7)
```

**Example 2** — huge exponent that O(exp) could never finish
```
base=2, exp=1000000000000000000, mod=1000000007 → 719476260
```

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: CLRS §31.6
