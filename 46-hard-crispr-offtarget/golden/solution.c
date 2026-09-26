#include "solution.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

void input_parse(const JsonValue *root, Input *in) {
	in->d = (int)json_int(json_get(root, "d"));
	in->len = (int)json_int(json_get(root, "len"));
	in->genome = json_str(json_get(root, "genome"));
	const JsonValue *guides = json_get(root, "guides");
	in->guides_len = json_len(guides);
	in->guides = (const char **)xmalloc(in->guides_len * sizeof *in->guides);
	for (size_t i = 0; i < in->guides_len; i++) {
		in->guides[i] = json_str(json_at(guides, i));
	}
}

void input_free(Input *in) {
	free(in->guides);
	in->guides = NULL;
	in->guides_len = 0;
	in->genome = NULL;
}

// A base as two bits: bits 1-2 of the ASCII code already tell A, C, G, and T
// apart (0, 1, 3, 2).
static uint64_t base_code(char c) {
	return (uint64_t)((c >> 1) & 3);
}

Answer solve(const Input *in) {
	const size_t n = strlen(in->genome);
	const size_t len = (size_t)in->len;
	Answer a = {(long long *)xcalloc(in->guides_len, sizeof *a.v), in->guides_len};
	if (n < len) {
		return a;
	}
	const size_t windows = n - len + 1;

	// Every window as one number, its base i in bits 2i and 2i+1, built one
	// offset at a time: pass i ORs base s + i into window s for every s, so no
	// window waits on the one before it. The bases are widened to 64 bits
	// first; built from the bytes, clang loads each four with vmovd, an
	// element load `make vec` counts.
	uint64_t *base = (uint64_t *)xmalloc(n * sizeof *base);
	for (size_t p = 0; p < n; p++) {
		base[p] = base_code(in->genome[p]);
	}
	uint64_t *code = (uint64_t *)xcalloc(windows, sizeof *code);
	for (size_t i = 0; i < len; i++) {
		for (size_t s = 0; s < windows; s++) {
			code[s] |= base[s + i] << (2 * i);
		}
	}

	// A window and a guide differ at base i where bit pair i of their XOR is
	// nonzero. Folding each pair onto its low bit leaves one bit per mismatch,
	// counted in-lane: x86-64-v3 has no packed popcount, and gcc 12 does not
	// vectorize __builtin_popcountll.
	const uint64_t d = (uint64_t)in->d;
	for (size_t k = 0; k < in->guides_len; k++) {
		uint64_t want = 0;
		for (size_t i = 0; i < len; i++) {
			want |= base_code(in->guides[k][i]) << (2 * i);
		}
		long long count = 0;
		for (size_t s = 0; s < windows; s++) {
			const uint64_t x = code[s] ^ want;
			uint64_t m = (x | x >> 1) & 0x5555555555555555ull;
			m = (m & 0x3333333333333333ull) + (m >> 2 & 0x3333333333333333ull);
			m = (m + (m >> 4)) & 0x0f0f0f0f0f0f0f0full;
			m += m >> 8;
			m += m >> 16;
			m += m >> 32;
			count += (m & 0xff) <= d;
		}
		a.v[k] = count;
	}

	free(code);
	free(base);
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	for (size_t i = 0; i < a->n; i++) {
		if (i > 0) {
			fputc(' ', out);
		}
		fprintf(out, "%lld", a->v[i]);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	free(a->v);
	a->v = NULL;
	a->n = 0;
}
