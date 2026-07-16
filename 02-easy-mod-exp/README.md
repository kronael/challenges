# 02 — Easy — Modular Power

**Task**: Compute `(base^exp) mod m` where `exp` can be up to 10^18.

**Difficulty**: easy
**Time estimate**: ~20 min

## Problem

Given three integers `base`, `exp`, and `mod`, compute `(base^exp) mod m`.

When `exp = 0`, return `1 % mod`. This is `0` when `mod = 1` and `1`
otherwise, including when `base = 0`.

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

**Example 2**
```
base=2, exp=1000000000000000000, mod=1000000007 → 719476260
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.
