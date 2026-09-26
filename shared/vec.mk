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
export CARGO_PROFILE_RELEASE_DEBUG := line-tables-only
else ifneq ($(wildcard go.mod),)
VEC_BIN  := ./$(MOD_NAME)
VEC_FUNC := main.solve
else
VEC_BIN  := ./main
VEC_FUNC := solve

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
	  --input $(VEC_INPUT) --units '$(VEC_UNITS)' --expect $(VEC_EXPECT)
