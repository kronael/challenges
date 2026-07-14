# Hints — 15 Medium — Matrix Exponentiation

> Spoilers. Open only when stuck.

- **Recurrence as matrix power**: `[[1,1],[1,0]]^n` holds `F(n)` in a corner; any
  linear recurrence becomes a matrix raised to a power.
- **O(log n) via squaring**: exponentiation-by-squaring on the transition matrix
  (equivalently fast doubling) turns an O(n) scan into O(log n) multiplies.
- **Keep everything reduced**: reduce after every multiply so the operands never
  exceed the modulus, and use a 64-bit (or wider) product so the intermediate
  multiplication doesn't overflow before the `% MOD`.

The naive O(n) iteration (loop `n` times accumulating `a, b = b, a+b mod MOD`) is
what `rotten/main.py` does — correct but it TIMEOUTs on the large cases.
