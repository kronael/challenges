# `make vec`: check this directory's build on every ../cases fixture and on
# VEC_INPUT, then trace solve on VEC_INPUT with scripts/vec_check.py, whose
# docstring states the grade.
#
# The including Makefile builds every target for x86-64-v3 and sets
# VEC_EXPECT := vectorized | scalar. The challenge's own vec.mk sets VEC_INPUT
# and VEC_UNITS, the unit of work: an input field's length or integer value, or
# a product a*b.

include ../vec.mk

ifneq ($(wildcard Cargo.toml),)
VEC_BIN  := target/release/$(BIN_NAME)
VEC_FUNC := solve
else ifneq ($(wildcard go.mod),)
VEC_BIN  := /tmp/$(MOD_NAME)-build
VEC_FUNC := main.solve
else
VEC_BIN  := ./main
VEC_FUNC := solve
endif

.PHONY: vec
vec: build
	@for f in ../cases/*.in $(VEC_INPUT); do \
	  $(VEC_BIN) < "$$f" | cmp -s - "$${f%.in}.out" \
	    || { echo "  $(VEC_BIN) printed the wrong answer for $$f"; exit 1; }; \
	done
	@python3 ../../scripts/vec_check.py --binary $(VEC_BIN) --function $(VEC_FUNC) \
	  --input $(VEC_INPUT) --units '$(VEC_UNITS)' --expect $(VEC_EXPECT)
