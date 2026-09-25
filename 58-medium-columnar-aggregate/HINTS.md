# Hints — 58 Medium — Variant Allele Counts

> Spoilers. Open only when stuck.

- **The answer is not in the arithmetic.** Two comparisons, a multiply and two
  running sums is already as small as a loop body gets, and nothing in it
  forbids doing eight samples at once: integer addition is associative, so the
  compiler is free to split the totals across lanes. Look at where the operands
  live instead.
- **Count the loads for one sample.** `in->sample[i]` is a pointer. Reading one
  genotype costs a load of that pointer and then a load through it. The compiler
  cannot know where sample `i+1`'s record sits until it has read sample `i`'s
  pointer, so two samples' fields can never become one vector load. This is not
  the cost model declining a slow lowering — there is no lowering. Confirm it:
  `cc -O3 -march=x86-64-v3 -fopt-info-vec-missed -S solution.c` prints
  `couldn't vectorize loop` and stays silent about any alternative.
- **You are allowed to touch the data twice.** A second `O(n)` pass is not a
  regression if it changes what the hardware can do with the first one.

## Approach

Walk the samples once and copy the three fields of every called sample into
three plain arrays — genotype, depth, quality — one element per called sample,
no gaps and no absences. Then aggregate over those arrays:

```c
for (size_t i = 0; i < called; i++) {
	const int32_t keep = (quality[i] >= qmin) & (depth[i] >= dmin);
	alt += keep * genotype[i];
	kept += keep;
}
```

Every operand is a unit-stride read, and `keep` is `0` or `1`, so the filter is
a multiply instead of a branch — nothing left for the compiler to if-convert.
gcc 12 turns this body into `vpminsd` / `vpcmpeqd` / `vpmulld` / `vpaddd` over
eight samples at a time, with a horizontal sum and a remainder tail outside the
loop. `AN` is `2 × kept`; computing it once at the end keeps a second multiply
out of the lanes.

The copy pass stays scalar, and that is fine. `make vec` looks for *one* loop
whose arithmetic is entirely packed, not for a function with no scalar loops.

## Why it is the layout and not the loop

The two implementations run the same comparisons on the same values in the same
order and return the same answer. `golden/` does strictly *more* work: an extra
pass, three allocations, `3n` copies. It wins because the shape it leaves behind
is one the vectorizer can use, and the control's is not. That is the whole
lesson — at this size the layout of the operands decides the throughput, and the
arithmetic does not.

Real genotype formats already made this trade. BCF, the binary form of VCF,
stores the per-sample fields *by field* rather than by sample: "Genotype fields
are encoded not by sample as in VCF but rather by field, with a vector of values
for each sample following each field" (VCFv4.3 §6.3.2). PLINK's `.bed` is
variant-major — one contiguous block of every sample's genotype per variant —
and PLINK 1.9 silently rewrites the older sample-major files into that order
when it meets them. Both formats pay a transpose once, at write time, so that
every per-variant scan afterwards streams.

## Complexity

Two `O(n)` passes and `O(n)` extra space, against the control's single `O(n)`
pass in `O(1)` space. There is no asymptotic gap to hide behind: this is the
same algorithm twice, and only the memory layout differs.

## Rust

The columnar loop has to be free of bounds checks to vectorize. Measured here
with `cargo rustc --release -C target-cpu=x86-64-v3`: indexing three separately
built `Vec`s by `i` stayed scalar, because the lengths are not known to agree;
zipping the three iterators vectorized. Collecting into a fixed-length slice
first works too.

`solve` carries `#[no_mangle]` so the symbol survives into the assembly for
`make vec` to find. Leave it on.

## Measured on this box — gcc 12.2, Debian

- The control stays scalar even at `-fvect-cost-model=unlimited`. Pointer
  indirection is a capability wall, not a price.
- Contiguous records are *not* a wall. An array of `{int32 genotype; int32
  depth; int32 quality;}` structs vectorizes at `-O3` — gcc SLP-permutes the
  stride-3 loads. A flat table with a run-time record stride is not a wall
  either: `-O3` implies `-fversion-loops-for-strides`, which emits a
  unit-stride clone of the loop and vectorizes that. Neither would make an
  honest control.
- `shared/c/io.mk` defaults to `-O2`, and `-O2` implies
  `-fvect-cost-model=very-cheap`, which refuses any loop whose trip count is
  not a known multiple of the vector width. Nothing here vectorizes at `-O2`,
  which is why all four Makefiles pin `-O3 -march=x86-64-v3` — the same flags
  `scripts/vec_check.py` compiles with, so `make test` and `make vec` read one
  build.

## Sources

- [VCF/BCF specification v4.3, §6.3.2 Genotype
  encoding](https://samtools.github.io/hts-specs/VCFv4.3.pdf)
- [PLINK 1.9 file formats — `.bed`](https://www.cog-genomics.org/plink/1.9/formats#bed)
- [GCC optimize options — `-fvect-cost-model`,
  `-fversion-loops-for-strides`](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)
