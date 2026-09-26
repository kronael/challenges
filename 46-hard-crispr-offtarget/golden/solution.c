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

// Windows per tile. A tile's codes stay in L1 while every guide sweeps them.
enum { TILE = 2048 };

Answer solve(const Input *in) {
	const size_t n = strlen(in->genome);
	const size_t len = (size_t)in->len;
	const size_t guides = in->guides_len;
	Answer a = {(long long *)xcalloc(guides, sizeof *a.v), guides};
	if (n < len) {
		return a;
	}
	const size_t windows = n - len + 1;

	uint64_t *want = (uint64_t *)xcalloc(guides, sizeof *want);
	for (size_t k = 0; k < guides; k++) {
		for (size_t i = 0; i < len; i++) {
			want[k] |= base_code(in->guides[k][i]) << (2 * i);
		}
	}

	const uint64_t d = (uint64_t)in->d;
	uint64_t base[TILE + 32];
	uint64_t code[TILE];
	for (size_t t = 0; t < windows; t += TILE) {
		const size_t w = windows - t < TILE ? windows - t : TILE;

		// Every window as one number: its base i in bits 2i and 2i+1. The code
		// of window s is built from s alone, one pass per offset i, so no
		// window waits on the one before it and consecutive windows are lanes
		// of one vector. Each base is widened to 64 bits once, so the passes
		// load whole vectors of codes: built straight from the genome's bytes,
		// clang loads four bytes at a time with vmovd, an element load
		// `make vec` counts.
		for (size_t p = 0; p < w + len - 1; p++) {
			base[p] = base_code(in->genome[t + p]);
		}
		for (size_t s = 0; s < w; s++) {
			code[s] = base[s];
		}
		for (size_t i = 1; i < len; i++) {
			for (size_t s = 0; s < w; s++) {
				code[s] |= base[s + i] << (2 * i);
			}
		}

		// A window and a guide differ at base i exactly when bit pair i of
		// their XOR is nonzero. Folding each pair onto its low bit leaves one
		// bit per mismatch, and the count is summed in-lane with shifts and
		// adds: x86-64-v3 has no packed popcount, and gcc does not vectorize
		// __builtin_popcountll.
		for (size_t k = 0; k < guides; k++) {
			long long count = 0;
			for (size_t s = 0; s < w; s++) {
				const uint64_t x = code[s] ^ want[k];
				uint64_t m = (x | x >> 1) & 0x5555555555555555ull;
				m = (m & 0x3333333333333333ull) + (m >> 2 & 0x3333333333333333ull);
				m = (m + (m >> 4)) & 0x0f0f0f0f0f0f0f0full;
				m += m >> 8;
				m += m >> 16;
				m += m >> 32;
				count += (m & 0xff) <= d;
			}
			a.v[k] += count;
		}
	}

	free(want);
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
