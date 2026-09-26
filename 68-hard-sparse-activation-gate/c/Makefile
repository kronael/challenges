# Two targets grade this directory. `make test` checks the answer against
# ../cases; `make vec` runs the same ./main on one fixture and checks that solve
# does its per-element work in packed SIMD lanes. -O3 -march=x86-64-v3 is the
# target `make vec` grades.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra

VEC_EXPECT := vectorized
LARGE_CASES := none

include ../../shared/c/io.mk
include ../../shared/vec.mk
