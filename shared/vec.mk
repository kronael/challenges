# Shape assertion for vec challenges: did the hot loop compile to packed SIMD?
#
# A vec challenge grades the emitted code, not the clock. Its golden reference
# must vectorize and its rotten control must not, and both have the same
# complexity, so a timing gate cannot tell them apart.
#
# A golden/ or rotten/ Makefile sets two variables and includes this file:
#
#   VEC_FUNCS  := dot_product           symbols to inspect
#   VEC_EXPECT := vectorized | scalar   what this directory must compile to
#   VEC_LANG   := c | rust | go         inferred from Cargo.toml or go.mod when unset
#
# This adds only the `vec` target, so it composes with shared/c/io.mk without
# colliding on build, test, bench, or clean.

.PHONY: vec

VEC_LANG   ?= $(if $(wildcard Cargo.toml),rust,$(if $(wildcard go.mod),go,c))
VEC_EXPECT ?= vectorized
VEC_ROOT   := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)

vec:
	@test -n "$(VEC_FUNCS)" || { echo "vec: set VEC_FUNCS in this Makefile"; exit 1; }
	@python3 $(VEC_ROOT)/scripts/vec_check.py --lang $(VEC_LANG) --expect $(VEC_EXPECT) \
	  $(foreach f,$(VEC_FUNCS),--function $(f))
