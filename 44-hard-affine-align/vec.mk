# `make vec` traces solve on this fixture and divides its scalar work by the
# length of s times the length of t.
VEC_INPUT := ../vec.in
VEC_UNITS := s*t
# gcc 12.2 -O3 loop distribution miscompiles a correct solve, so every C build
# here, golden/'s included, turns it off where the compiler accepts the flag.
VEC_CFLAGS = $(shell $(CC) -fno-tree-loop-distribution -E -x c /dev/null >/dev/null 2>&1 && echo -fno-tree-loop-distribution)
