# Hints — 67 Medium — Tick Frame Audit

> Spoilers. Open only when stuck.

- **The answer is not in the classification.** Two compares name a byte, one
  more compare checks it against what its offset requires, and a running count
  of the mismatches is all the arithmetic there is. Nothing in it forbids
  checking thirty-two bytes at once. Look at what the loop carries from one
  byte to the next instead.
- **Ask what `pos` is.** A cursor that ticks up and wraps at `width` is a value
  the compiler can only produce by running the previous iteration: it is
  neither an induction variable nor a reduction. Confirm it: `cc -O3
  -march=x86-64-v3 -fopt-info-vec-missed -S solution.c` reports `unsupported
  use in stmt` for the byte loop, and `control flow in loop` as well when a
  `switch` sits in it.
- **The offset is arithmetic on the index, not state.** Frame `f` starts at
  `f × width`, and its byte `j` sits at offset `j`. Neither needs the previous
  byte.

## Approach

Lay out the class every offset must hold, once:

```c
uint8_t *expect = xcalloc(width, 1); /* PAYLOAD */
for (size_t k = 0; k < separators_len; k++) {
	expect[separators[k]] = SEPARATOR;
}
expect[width - 1] = TERMINATOR;
```

Then walk the stream frame by frame, and inside a frame offset by offset:

```c
for (size_t f = 0; f < frames; f++) {
	const uint8_t *rec = stream + f * width;
	uint32_t mism = 0;
	for (size_t j = 0; j < width; j++) {
		const uint8_t cls = (rec[j] == '|') * SEPARATOR + (rec[j] == '\n') * TERMINATOR;
		mism += cls != expect[j];
	}
	stray += mism;
	clean += mism == 0;
}
```

Every operand of the inner loop is a unit-stride read, a byte's class is two
compares folded into a number, and the check is one more compare summed into a
counter. gcc 12 turns this body into `vpcmpeqb` / `vpand` / `vpandn` /
`vpsubb` over thirty-two bytes at a time, widens the mismatch bytes with
`vpmovzxbw` / `vpmovzxwd` into `vpaddd`, and leaves the horizontal sum and the
remainder tail outside the loop. Whether the frame is clean is decided once per
frame, outside the lanes.

The template pass stays scalar, and that is fine. `make vec` looks for *one*
loop whose arithmetic is entirely packed, not for a function with no scalar
loops.

## Why it is the shape and not the work

Both implementations run the same three compares on every byte and return the
same answer. `golden/` does no less work: the same `O(bytes)` walk and the same
template. It wins because the inner loop's trip count is `width` and every
operand's address follows from the loop index alone, so thirty-two consecutive
bytes can be classified side by side; the control's cursor makes byte `i+1`'s
offset depend on byte `i`'s, and its `switch` is control flow the vectorizer
will not fold into a select.

This is the shape a feed handler ends up with once the per-byte `switch` shows
up in a profile. A fixed-width layout exists so that record boundaries and
field offsets are known before a byte is read; the handler that still discovers
them by walking a cursor pays for state it already had. Compare-against-a-
constant over a block of bytes is the same move simdjson makes to find its
structural characters: sixty-four bytes go through one compare, and the result
is a mask, not a branch.

## Complexity

`O(bytes)` time for both, plus `O(width)` extra space for the template. There
is no asymptotic gap to hide behind: this is the same algorithm twice, and only
the control shape differs.

## Rust

Measured here with `cargo rustc --release -C target-cpu=x86-64-v3`:
`stream.chunks_exact(width)` with the frame's bytes zipped against the template
vectorized, and so did indexing `rec[j]` and `expect[j]` by `j` inside a
`for j in 0..width` — the chunk and the template have the same length, so LLVM
hoists the bounds checks. A `for &b in stream` walk with a `match` on the byte
and a wrapping `pos` stayed scalar, like the C control.

`solve` carries `#[no_mangle]` so the symbol survives into the assembly for
`make vec` to find. Leave it on.

## Measured on this box — gcc 12.2, Debian

- The control stays scalar at `-fvect-cost-model=unlimited`. Both of its walls
  are capability walls, not prices.
- The cursor alone is a wall. Keeping `pos` and replacing the `switch` with the
  branchless class still reports `unsupported use in stmt`.
- The `switch` alone is a wall. The frame-major nested loop with a `switch`
  inside stays scalar (`control flow in loop`), while the same nested loop with
  an `if` / `else if` chain, or a ternary, that *assigns the class* vectorizes:
  gcc if-converts a branch that computes a value, not a `switch`.
- `expect[i % width]` in a flat loop is not a way out either: gcc reports `not
  suitable for gather load` and stays scalar.
- `shared/c/io.mk` defaults to `-O2`, and `-O2` implies
  `-fvect-cost-model=very-cheap`, which refuses any loop whose trip count is
  not a known multiple of the vector width. Nothing here vectorizes at `-O2`,
  which is why all four Makefiles pin `-O3 -march=x86-64-v3` — the same flags
  `scripts/vec_check.py` compiles with, so `make test` and `make vec` read one
  build.

## Sources

- Geoff Langdale and Daniel Lemire, "Parsing Gigabytes of JSON per Second",
  The VLDB Journal 28 (2019) — structural characters located by comparing
  blocks of bytes against constants and keeping the result as a bitmask.
  [arXiv:1902.08318](https://arxiv.org/abs/1902.08318)
- [Auto-vectorization in GCC](https://gcc.gnu.org/projects/tree-ssa/vectorization.html)
  — the loop shapes the vectorizer handles and the dependences it does not
- [GCC optimize options — `-fopt-info`,
  `-fvect-cost-model`](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)
