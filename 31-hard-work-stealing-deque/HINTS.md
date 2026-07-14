# Hints — 31 Hard — Chase-Lev Work-Stealing Deque

> Spoilers. Open only when stuck.

- **Last-element race**: the owner speculatively decrements `bottom`, reads the
  slot, then CASes `top`. On CAS success the owner keeps the element; on CAS
  failure a thief took it first, so the owner returns `Empty` and restores
  `bottom` to the empty position.
- **The Dekker moment**: the owner's `bottom` store and the thief's `top` load
  form a Dekker pattern — only `SeqCst` on the decisive `top` CAS (and a
  `SeqCst` fence on the steal side, between loading `top` and `bottom`) stops
  both sides from claiming the same element. Acquire/Release alone is not enough
  here on a weak memory model.
- **Suggested orderings**: `push` writes the slot then stores `bottom` with
  `Release`. `pop` stores the decremented `bottom` with `SeqCst`, loads `top`
  with `SeqCst` (or `Acquire`), and the last-element CAS on `top` is `SeqCst`.
  `steal` loads `top` with `Acquire`, then a `SeqCst` fence, then loads `bottom`
  with `Acquire`, and CASes `top` with `SeqCst`.
- **ABA**: in this formulation `top` and `bottom` are monotonically increasing
  indices, so a stale `top` value cannot be mistaken for a fresh one — the
  Chase-Lev trick is that no separate tag field is needed.
- **Steal return values**: distinguish "deque empty" (`Empty`) from "lost the
  CAS, try again" (`Retry`). Thieves spin on `Retry` and only give up on
  `Empty` once the owner signals it is done producing.

Source: [Chase & Lev, *Dynamic Circular Work-Stealing Deque* (SPAA 2005)](https://www.di.ens.fr/~zappa/readings/ppopp13.pdf)
