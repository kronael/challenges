# The shape check compiles this directory by itself, so the shared JSON reader
# and allocation helpers have to be reachable without io.mk's -I flags.
export C_INCLUDE_PATH := $(abspath ../../shared/c)

# Two targets grade this directory. `make test` checks the answer against
# ../cases; `make vec` checks the shape of the code that produced it. -O3
# -march=x86-64-v3 matches what scripts/vec_check.py compiles, so both read the
# same build.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra

VEC_FUNCS  := solve
VEC_EXPECT := vectorized

include ../../shared/c/io.mk
include ../../shared/vec.mk
