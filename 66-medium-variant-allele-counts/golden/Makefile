# -O3 -march=x86-64-v3 is the target `make vec` grades, and `make vec` traces the
# ./main this builds, so the fixture suite and the grade check one build. The
# intrinsics in solution.c need AVX2, which x86-64-v3 carries.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra

VEC_EXPECT := vectorized

include ../../shared/c/io.mk
include ../../shared/vec.mk

.PHONY: regen
regen: build
	@for f in ../cases/[0-9]*.in; do \
	  ./main < "$$f" > "$${f%.in}.out"; \
	  echo "  $$(basename $$f) → done"; \
	done
