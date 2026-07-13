# Hints — 19 Fast Modular Exponentiation

> Spoilers. Open only when stuck.

- **Repeated squaring**: square the base and consume one bit of the exponent per
  step, halving the problem each time — O(log exp) instead of O(exp). That turns
  10^18 multiplications into about 60.
- **Modular arithmetic discipline**: reduce mod `m` after every multiply so
  intermediate values stay bounded and never overflow the word size.
- **Watch the multiply itself**: with `mod` up to 10^18, two reduced values can
  still be ~10^18 each, and their product overflows 64 bits before the mod. In
  Python this is free; in Go/Rust use a 128-bit intermediate (or `math/big` /
  `u128`) for the multiply, or you will get a wrong answer that looks plausible.

The naive O(exp) loop (`for _ in range(exp): result = result * base % mod`) is
what `rotten/main.py` does — correct on tiny exponents but it TIMEOUTs on the
large cases.

Source: CLRS §31.6
