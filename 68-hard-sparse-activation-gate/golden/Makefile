# The shape check compiles this directory by itself, so the shared JSON reader
# and allocation helpers have to be reachable without io.mk's -I flags.
export C_INCLUDE_PATH := $(abspath ../../shared/c)

# -O3 -march=x86-64-v3 is what scripts/vec_check.py compiles, so the fixture suite
# runs the same code the shape check reads. The intrinsics in solution.c need
# AVX2, BMI2, and POPCNT, and x86-64-v3 is the baseline that carries all three.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra

VEC_FUNCS  := solve
VEC_EXPECT := vectorized

include ../../shared/c/io.mk
include ../../shared/vec.mk

.PHONY: regen
regen: build
	@for f in ../cases/[0-9]*.in; do \
	  ./main < "$$f" > "$${f%.in}.out"; \
	  echo "  $$(basename $$f) → done"; \
	done
