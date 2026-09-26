# `make vec` traces solve on this fixture and counts its scalar work per residue
# pair: one residue of s taken with one residue of t, |s|·|t| pairs in all.
VEC_INPUT := ../vec.in
VEC_UNITS := s*t
# gcc 12.2 -O3 loop distribution miscompiles a correct row-by-row solve.
VEC_CFLAGS = $(shell $(CC) -fno-tree-loop-distribution -E -x c /dev/null >/dev/null 2>&1 && echo -fno-tree-loop-distribution)
