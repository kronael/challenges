# Grading for vec challenges: does solve do its per-element work in packed lanes?
#
# A vec challenge grades the emitted code weighted by how often it runs, not the
# clock. `make vec` runs the program this directory builds on one fixture under
# scripts/vec_check.py, which single-steps the call to solve and counts the
# scalar work it retires per element of the input; that script's docstring
# states the rule. golden/ must stay within the budget and rotten/ must not.
#
# The challenge's own vec.mk, one directory up, names the traced fixture:
#
#   VEC_INPUT := ../cases/14.in   the fixture solve runs on
#   VEC_UNITS := dosage           the unit of work: an input array's length, an
#                                 integer field's value, or a product, a*b
#
# Every Makefile that includes this sets VEC_EXPECT := vectorized | scalar.
# The traced program is built for x86-64-v3, and `make vec` first checks its
# answer on every fixture in ../cases, so the graded build is one whose answers
# are checked. By default it is the program `make test` checks: ./main for C,
# the release build of src/main.rs for Rust, and the `build` output for Go. A
# Makefile whose `make test` keeps other flags sets VEC_BUILD, the target that
# builds its x86-64-v3 program, and VEC_BIN, the path it writes, before
# including this.
#
# This adds only the `vec` target, so it composes with shared/c/io.mk without
# colliding on build, test, bench, or clean.

.PHONY: vec

VEC_ROOT   := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
VEC_LANG   ?= $(if $(wildcard Cargo.toml),rust,$(if $(wildcard go.mod),go,c))

include ../vec.mk

ifeq ($(VEC_LANG),rust)
VEC_BUILD ?= build
VEC_BIN   ?= target/release/challenge
VEC_FUNC  := solve
else ifeq ($(VEC_LANG),go)
VEC_BUILD ?= build
VEC_BIN   ?= /tmp/$(MOD_NAME)-build
VEC_FUNC  := main.solve
else
VEC_BUILD ?= main
VEC_BIN   ?= ./main
VEC_FUNC  := solve
endif

vec: $(VEC_BUILD)
	@for f in ../cases/*.in; do \
	  $(VEC_BIN) < "$$f" | cmp -s - "$${f%.in}.out" \
	    || { echo "  $(VEC_BIN) printed the wrong answer for $$f"; exit 1; }; \
	done
	@python3 $(VEC_ROOT)/scripts/vec_check.py --binary $(VEC_BIN) --function $(VEC_FUNC) \
	  --input $(VEC_INPUT) --units '$(VEC_UNITS)' --expect $(VEC_EXPECT)
