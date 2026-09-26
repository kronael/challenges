include ../../shared/c/io.mk

# `make vec` grades its own build, ./main-vec, for x86-64-v3; `make test` and
# `make bench` keep ./main and its flags.
VEC_EXPECT := vectorized
VEC_BUILD  := main-vec
VEC_BIN    := ./main-vec

include ../../shared/vec.mk
