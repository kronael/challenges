# `make vec`: check this directory's build on every ../cases fixture and on
# VEC_INPUT, then trace solve on VEC_INPUT with scripts/vec_check.py, whose
# docstring states the grade. A C build hands it the compiler, flags, and
# sources of ./main, so it checks what the preprocessor leaves of them.
#
# This file sets the flags every target of the including Makefile builds with,
# so `make test`, `make bench`, and `make vec` check one program: x86-64-v3,
# with simd/archsimd for Go, line tables for Rust, and -O3 for C, where io.mk's
# -O2 pins -fvect-cost-model=very-cheap, which declines any loop whose trip
# count is not a known multiple of the vector width. override outranks the
# including Makefile and the command line, so a flag a solver adds there does
# not reach the build the grade traces.
#
# The including Makefile sets VEC_EXPECT := vectorized | scalar. The challenge's
# own vec.mk sets VEC_INPUT and VEC_UNITS, the unit of work: an input field's
# length or integer value, or a product a*b, and may set VEC_CFLAGS, flags its C
# build adds.

include ../vec.mk

ifneq ($(wildcard Cargo.toml),)
VEC_BIN  := target/release/$(BIN_NAME)
VEC_FUNC := solve
override RUSTFLAGS := -C target-cpu=x86-64-v3
override CARGO_PROFILE_RELEASE_DEBUG := line-tables-only
export RUSTFLAGS CARGO_PROFILE_RELEASE_DEBUG
unexport CARGO_ENCODED_RUSTFLAGS
else ifneq ($(wildcard go.mod),)
VEC_BIN  := ./$(MOD_NAME)
VEC_FUNC := main.solve
override GOAMD64 := v3
override GOEXPERIMENT := simd
override GOFLAGS :=
export GOAMD64 GOEXPERIMENT GOFLAGS
else
VEC_BIN  := ./main
VEC_FUNC := solve
override CC := $(firstword $(CC))
override CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra $(VEC_CFLAGS)
override CPPFLAGS :=
override LDLIBS :=
VEC_LINT = --cc '$(CC) $(CPPFLAGS) $(C_IO_CPPFLAGS) $(CFLAGS)' \
  --c-sources $(C_IO_DIR)/main.c solution.c

help::
	@echo "vec    — trace solve on one fixture and check its work runs in packed lanes"
endif

.PHONY: vec
vec: build
	@out=$$(mktemp); trap 'rm -f "$$out"' EXIT; \
	for f in ../cases/*.in $(VEC_INPUT); do \
	  timeout -k 2 10 $(VEC_BIN) < "$$f" > "$$out"; code=$$?; \
	  if [ $$code -eq 124 ] || [ $$code -eq 137 ]; then \
	    echo "  $(VEC_BIN) ran past 10 s on $$f"; exit 1; \
	  elif [ $$code -gt 128 ]; then \
	    echo "  $(VEC_BIN) crashed with SIG$$(kill -l $$code) on $$f"; exit 1; \
	  elif [ $$code -ne 0 ]; then \
	    echo "  $(VEC_BIN) exited with status $$code on $$f"; exit 1; \
	  fi; \
	  cmp -s "$$out" "$${f%.in}.out" \
	    || { echo "  $(VEC_BIN) printed the wrong answer for $$f"; exit 1; }; \
	done
	@python3 ../../scripts/vec_check.py --binary $(VEC_BIN) --function $(VEC_FUNC) \
	  --input $(VEC_INPUT) --units '$(VEC_UNITS)' --expect $(VEC_EXPECT) $(VEC_LINT)
