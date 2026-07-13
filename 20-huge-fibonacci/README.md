# 20 — Huge Fibonacci

**Task**: Compute the Nth Fibonacci number mod 10^9+7, where N can be as large as 10^18.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

The Fibonacci numbers are defined by `F(0) = 0`, `F(1) = 1`, and
`F(n) = F(n-1) + F(n-2)` for `n ≥ 2`. Given `n`, output `F(n) mod 1_000_000_007`.

Constraints: `0 ≤ n ≤ 10^18`.

## Input

```json
{"n": 10}
```

## Output

A single integer: `F(n) mod 1_000_000_007`.

## Examples

**Example 1**

Input:
```json
{"n": 10}
```

Output:
```text
55
```

**Example 2**

Input:
```json
{"n": 1000000000}
```

Output:
```text
21
```

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: competitive classic
