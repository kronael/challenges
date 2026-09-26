# Every target compiles at -O3 -march=x86-64-v3, the flags `make vec` grades,
# so `make test`, `make bench`, and `make vec` check one program.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra

VEC_EXPECT := vectorized

include ../../shared/c/io.mk
include ../../shared/vec.mk
