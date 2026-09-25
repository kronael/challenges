# The shape check compiles this directory by itself, so the shared JSON reader
# and allocation helpers have to be reachable without io.mk's -I flags.
export C_INCLUDE_PATH := $(abspath ../../shared/c)

# The control: same answer, same O(samples), and `make vec` must find its loop
# still in scalar registers. Built with the flags scripts/vec_check.py uses, so
# `make test` and `make vec` read the same build.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra

VEC_FUNCS  := solve
VEC_EXPECT := scalar

include ../../shared/c/io.mk
include ../../shared/vec.mk
