#include "solution.h"

#include <immintrin.h>
#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *scores = json_get(root, "scores");
	in->n = json_len(scores);
	in->score = (int32_t *)xmalloc(in->n * sizeof *in->score);
	for (size_t i = 0; i < in->n; i++) {
		in->score[i] = (int32_t)json_int(json_at(scores, i));
	}
	in->threshold = (int32_t)json_int(json_get(root, "threshold"));
}

void input_free(Input *in) {
	free(in->score);
	in->score = NULL;
	in->n = 0;
}

Answer solve(const Input *in) {
	const size_t n = in->n;
	const int32_t *score = in->score;
	int32_t *kept = (int32_t *)xmalloc(n * sizeof *kept);
	size_t k = 0;

	// Eight scores per step. The compare leaves one bit per lane in `m`, and
	// the permutation that packs the surviving lanes to the front is `m`
	// applied to the identity 0..7: pdep spreads the bits to one per byte and
	// pext compresses the identity bytes against them. The store writes all
	// eight lanes; popcount says how many count, and the next block or the
	// tail overwrites the rest.
	const __m256i limit = _mm256_set1_epi32(in->threshold);
	size_t i = 0;
	for (; i + 8 <= n; i += 8) {
		const __m256i v = _mm256_loadu_si256((const __m256i *)(score + i));
		const __m256i above = _mm256_cmpgt_epi32(v, limit);
		const unsigned m = (unsigned)_mm256_movemask_ps(_mm256_castsi256_ps(above));
		const uint64_t bytes = _pdep_u64(m, 0x0101010101010101ull) * 0xff;
		const uint64_t lanes = _pext_u64(0x0706050403020100ull, bytes);
		const __m256i perm = _mm256_cvtepu8_epi32(_mm_cvtsi64_si128((long long)lanes));
		_mm256_storeu_si256((__m256i *)(kept + k), _mm256_permutevar8x32_epi32(v, perm));
		k += (size_t)_mm_popcnt_u32(m);
	}
	for (; i < n; i++) {
		if (score[i] > in->threshold) {
			kept[k++] = score[i];
		}
	}

	Answer a = { kept, k };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	for (size_t i = 0; i < a->n; i++) {
		if (i > 0) {
			fputc(' ', out);
		}
		fprintf(out, "%d", a->kept[i]);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	free(a->kept);
	a->kept = NULL;
	a->n = 0;
}
