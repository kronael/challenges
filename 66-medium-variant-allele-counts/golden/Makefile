# shared/vec.mk sets the flags `make vec` grades, and `make vec` traces the
# ./main this builds, so the fixture suite and the grade check one build. The
# intrinsics in solution.c need AVX2, which x86-64-v3 carries.

VEC_EXPECT := vectorized
LARGE_CASES := none

include ../../shared/c/io.mk
include ../../shared/vec.mk

.PHONY: regen
regen: build
	@for f in ../cases/[0-9]*.in; do \
	  ./main < "$$f" > "$${f%.in}.out"; \
	  echo "  $$(basename $$f) → done"; \
	done
