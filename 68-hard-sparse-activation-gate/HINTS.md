# Hints — 68 Hard — Sparse Activation Gate

> Spoilers. Open only when stuck.

- **The compare is not the problem.** Eight `score > threshold` tests fit one
  `vpcmpgtd`, and the compiler emits it without being asked — for a loop that
  only *counts* the kept scores. Ask what it cannot emit for the loop that
  *writes* them.
- **Where does score `i` land?** At slot `k`, and `k` is how many of scores
  `0..i-1` were kept. Lane `i+1` cannot pick its address until lane `i` has
  decided, so the store index is a serial chain through the whole batch, and
  the vectorizer refuses it outright. Confirm it: `cc -O3 -march=x86-64-v3
  -fopt-info-vec-missed -S solution.c` prints `not vectorized: unsupported use
  in stmt` and stays silent about any alternative.
- **The chain is only eight lanes long at a time.** Within one vector, "how
  many before me" is a function of eight compare bits, and eight bits have 256
  values. Nothing has to be computed lane by lane at run time.

## Approach

This is stream compaction, and the classic parallel formulation has three
steps: flag every element, take the exclusive prefix sum of the flags, and
scatter each flagged element to its prefix sum. Inside one AVX2 vector the
three steps collapse into a compare, a bit mask, and a permute:

```c
const __m256i v = _mm256_loadu_si256((const __m256i *)(score + i));
const __m256i above = _mm256_cmpgt_epi32(v, limit);
const unsigned m = (unsigned)_mm256_movemask_ps(_mm256_castsi256_ps(above));
const uint64_t bytes = _pdep_u64(m, 0x0101010101010101ull) * 0xff;
const uint64_t lanes = _pext_u64(0x0706050403020100ull, bytes);
const __m256i perm = _mm256_cvtepu8_epi32(_mm_cvtsi64_si128((long long)lanes));
_mm256_storeu_si256((__m256i *)(kept + k), _mm256_permutevar8x32_epi32(v, perm));
k += (size_t)_mm_popcnt_u32(m);
```

`m` holds the eight flags. Lane `j`'s exclusive prefix sum is
`popcount(m & ((1 << j) - 1))`, and the scatter "lane `j` goes to slot
`prefix(j)`" is the same thing as the gather "slot `s` takes the `s`-th set
bit of `m`" — which is a permutation index vector. Two ways to get it:

- A table of 256 rows, each the indices of that mask's set bits packed to the
  front. Build it once with the scalar append loop: the naive code runs 256
  times in total, never per element.
- BMI2, which `x86-64-v3` includes. `pdep` spreads the eight bits to one per
  byte, `* 0xff` widens each to a full byte, `pext` compresses the identity
  bytes `07 06 05 04 03 02 01 00` against them, and `vpmovzxbd` widens the
  bytes to lanes. `pext` is itself a compaction, just of bits, so the
  permutation is the mask compressed against the identity.

`vpermd` applies the permutation. The store writes all eight lanes at
`kept + k`, and only `popcount(m)` of them count: the next block's store, or
the scalar tail, overwrites the rest. `kept` is sized `n`, and the block store
never runs past it because `k ≤ i ≤ n - 8` inside the loop. The tail of
`n mod 8` scores stays scalar, exactly like the control.

Across vectors the carry is the scalar `k`. That is the one serial dependency
left, and it is one add per eight scores instead of one per score.

## Why it is the shape and not the loop

The two implementations run the same compares on the same scores and write
the same values to the same slots. `golden/` does strictly *more* work per
score: a permute, a popcount, and a `pdep`/`pext` pair per block. It wins
because it took the per-lane position out of the loop-carried chain and turned
it into a function of the mask, and a function of the mask is something the
hardware can evaluate for eight lanes at once. The control asks the compiler
to discover that on its own, and gcc 12 does not — it says so and moves on.

Inference kernels make this move all the time. A mixture-of-experts router
scores every token for every expert and then hands each expert the tokens it
won, packed densely and in order — that packing is this loop. Contextual
sparsity does the same to neurons: predict which ones fire, gather them into a
dense block, run only that block. Both are sparse selection followed by a
dense write, and both live or die by whether the selection runs in lanes.

## Complexity

Both implementations are `O(n)` time and `O(n)` output. There is no asymptotic
gap to hide behind: this is the same algorithm twice, and only the shape of
the per-element position computation differs.

## Rust

The same intrinsics live in `std::arch::x86_64`: `_mm256_cmpgt_epi32`,
`_mm256_movemask_ps`, `_pdep_u64`, `_pext_u64`, `_mm256_cvtepu8_epi32`,
`_mm256_permutevar8x32_epi32`. Put the kernel in an `unsafe fn` marked
`#[target_feature(enable = "avx2,bmi2,popcnt")]`, call it from `solve` behind
`is_x86_feature_detected!`, and keep the scalar append as the other branch.
Measured here with `cargo rustc --release -- -C target-cpu=x86-64-v3`: the
kernel inlines into `solve` and reports `6p/0s 0p/0s 0p/0s -> vectorized`.
`cargo test` builds without that flag, so the detection branch is what lets
the test binary run the kernel at all.

`solve` carries `#[no_mangle]` so the symbol survives into the assembly for
`make vec` to find. Leave it on.

## Measured on this box — gcc 12.2, Debian

- The control stays scalar at `-march=x86-64-v4` too. AVX-512 has
  `vpcompressd`, which is this loop in one instruction, and gcc 12's
  vectorizer still reports `unsupported use in stmt` and emits no compress.
  The wall is the vectorizer's analysis, not the instruction set.
- The three-pass plain-C form — a `keep[i]` flag array, a prefix-sum array,
  then `out[pos[i]] = x[i]` for every `i` — vectorizes only its first pass.
  The prefix loop is a loop-carried dependence (`possible dependence between
  data-refs`), and the scatter store has no AVX2 instruction to lower to
  (`possible alias involving gather/scatter`). It is the right decomposition
  and the wrong granularity: the prefix sum has to happen inside a vector, not
  across an array.
- `shared/c/io.mk` defaults to `-O2`, which is why all four Makefiles pin
  `-O3 -march=x86-64-v3` — the same flags `scripts/vec_check.py` compiles
  with, so `make test` and `make vec` read one build. Here the flag also
  matters for a second reason: the intrinsics need AVX2, BMI2, and POPCNT, and
  `x86-64-v3` is the baseline that carries all three.

## Sources

- Peter Cordes, [AVX2 what is the most efficient way to pack left based on a
  mask?](https://stackoverflow.com/questions/36932240) — the `pdep`/`pext`
  permutation and the 256-entry table it replaces
- Guy E. Blelloch, [Prefix Sums and Their
  Applications](https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf) (1990) — the
  flag / scan / scatter formulation
- Harris, Sengupta, Owens, [Parallel Prefix Sum (Scan) with
  CUDA](https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda),
  GPU Gems 3 ch. 39 — stream compaction as an application of scan
- [Intel Intrinsics
  Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html)
  — `_mm256_permutevar8x32_epi32`, `_pdep_u64`, `_pext_u64`
- Shazeer et al., [Outrageously Large Neural Networks: The Sparsely-Gated
  Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538) (2017) — the
  router that produces this batch
- [GCC optimize options —
  `-fvect-cost-model`](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)
