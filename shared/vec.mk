# `make vec`: check this directory's x86-64-v3 build on every ../cases fixture,
# then trace solve on VEC_INPUT with scripts/vec_check.py, whose docstring
# states the grade.
#
# The including Makefile sets VEC_EXPECT := vectorized | scalar. The
# challenge's own vec.mk sets VEC_INPUT and VEC_UNITS, the unit of work: an
# input field's length or integer value, or a product a*b. The graded build is
# the one `make test` checks unless the Makefile sets VEC_BUILD, the target
# that builds for x86-64-v3, and VEC_BIN, what it writes.

include ../vec.mk

ifneq ($(wildcard Cargo.toml),)
VEC_BUILD ?= build
VEC_BIN   ?= target/release/challenge
VEC_FUNC  := solve
else ifneq ($(wildcard go.mod),)
VEC_BUILD ?= build
VEC_BIN   ?= /tmp/$(MOD_NAME)-build
VEC_FUNC  := main.solve
else
VEC_BUILD ?= main
VEC_BIN   ?= ./main
VEC_FUNC  := solve
endif

.PHONY: vec
vec: $(VEC_BUILD)
	@for f in ../cases/*.in; do \
	  $(VEC_BIN) < "$$f" | cmp -s - "$${f%.in}.out" \
	    || { echo "  $(VEC_BIN) printed the wrong answer for $$f"; exit 1; }; \
	done
	@python3 ../../scripts/vec_check.py --binary $(VEC_BIN) --function $(VEC_FUNC) \
	  --input $(VEC_INPUT) --units '$(VEC_UNITS)' --expect $(VEC_EXPECT)
