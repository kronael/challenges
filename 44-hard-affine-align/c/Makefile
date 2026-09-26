# Every target compiles at -O3 -march=x86-64-v3, the flags `make vec` grades,
# so `make test`, `make bench`, and `make vec` check one program.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra
# gcc 12.2 -O3 loop distribution miscompiles a correct row-by-row solve.
CFLAGS += $(shell $(CC) -fno-tree-loop-distribution -E -x c /dev/null >/dev/null 2>&1 && echo -fno-tree-loop-distribution)

VEC_EXPECT := vectorized

include ../../shared/c/io.mk
include ../../shared/vec.mk
