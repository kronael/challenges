# 19 — Fast Modular Exponentiation

Compute `(base ^ exp) mod m` where `exp` can be a billion. The trick is reaching the answer in O(log exp) multiplications while never overflowing.

## Input / Output

```
{"base":<int>,"exp":<int>,"mod":<int>}
---
<value>      (base ^ exp) mod m
```

## Example

```
{"base":3,"exp":5,"mod":7}
→ 5      (243 mod 7)
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
