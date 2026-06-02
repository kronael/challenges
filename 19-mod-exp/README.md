# 19 — Fast Modular Exponentiation

Compute `(base ^ exp) mod m` for non-negative `base`, `exp` and `m ≥ 1`.

## Input / Output

```
{"base":<int>,"exp":<int>,"mod":<int>}
---
<value>      (base ^ exp) mod m
```

## Examples

```
{"base":2,"exp":1000000000,"mod":1000000007}
→ 140625001

{"base":3,"exp":5,"mod":7}
→ 5
```

## Key insight

Exponentiation by squaring: square the base and consume one bit of the exponent per step, multiplying into the result on set bits. O(log exp) multiplications, all reduced mod m.

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```
