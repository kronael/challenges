# 19 — Fast Modular Exponentiation

**Task**: Compute (base^exp) mod m where exp can be up to 10^18.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Compute `(base^exp) mod m` where `exp` can be 10^18. Multiplying base by itself exp times would take 10^18 steps — hopeless. You need O(log exp). And you must reduce mod `m` after *every* multiply: skip that and the intermediate products overflow a 64-bit word long before you finish.

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
base=2, exp=1000000000000000000, mod=1000000007 → 286130418
```

## Teaches

- **Repeated squaring**: square the base and consume one bit of the exponent per step, halving the problem each time — O(log exp) instead of O(exp).
- **Modular arithmetic discipline**: reduce mod `m` after every multiply so intermediate values stay bounded and never overflow the word size.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: CLRS §31.6
