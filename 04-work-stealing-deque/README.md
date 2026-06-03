# 04 — Chase-Lev Work-Stealing Deque

Owner `push`/`pop` at the bottom; any number of thieves `steal` from the top; atomics only.
Hard because when one element remains (`bottom - top == 1`) the owner's `pop` and a thief's `steal` race for the same slot, and exactly one may win.

## Teaches

- **Last-element race**: owner speculatively decrements `bottom`, reads the slot, then CASes `top`; on CAS failure a thief took it, so it returns Empty and restores `bottom`.
- **The Dekker moment**: the owner's `bottom` store and the thief's `top` load form a Dekker pattern — only `SeqCst` on the decisive `top` CAS stops both from reading the stale value and both claiming the element.
- **ABA**: `top` must carry a tag so a stale read isn't mistaken for fresh.

## Run
```
cd rust && make
```
Source: [Chase & Lev, *Dynamic Circular Work-Stealing Deque* (SPAA 2005)](https://www.di.ens.fr/~zappa/readings/ppopp13.pdf)
