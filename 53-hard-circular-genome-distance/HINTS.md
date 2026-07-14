# Hints — 53 Hard — Circular Genome Distance

> Spoilers. Open only when stuck.

- Replace every signed block with two extremity nodes. A positive block `i`
  becomes `(2i-1, 2i)` and a negative block becomes `(2i, 2i-1)`.
- Join the right extremity of each block to the left extremity of the next block
  on the same circular chromosome. Do this once for each genome.
- The two edge sets form a 2-regular breakpoint graph. Every connected component
  is an alternating cycle.
- If there are `n` blocks and `c` alternating cycles, the distance is `n-c`.
  Store each color as a node-to-partner table so cycle counting is linear.
- A linear search for the partner of every visited extremity is still correct,
  but takes quadratic time. That is the implementation in `rotten/main.py`.

Sources:

- [Yancopoulos, Attie, and Friedberg — Efficient sorting of genomic permutations](https://doi.org/10.1093/bioinformatics/bti535)
- [Alekseyev and Pevzner — Multi-break rearrangements and chromosomal evolution](https://doi.org/10.1016/j.tcs.2008.01.013)
