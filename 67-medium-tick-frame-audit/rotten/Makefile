# The control: the same answer in the same O(n), and `make vec` must find its
# per-element work still in scalar registers. Built for the target `make vec`
# grades, and traced as built, so `make test` and `make vec` check one build.
CFLAGS := -std=c11 -O3 -march=x86-64-v3 -g -Wall -Wextra

VEC_EXPECT := scalar

include ../../shared/c/io.mk
include ../../shared/vec.mk
