#include "solution.h"

#include <immintrin.h>
#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *dosage = json_get(root, "dosage");
	const JsonValue *depth = json_get(root, "depth");
	const JsonValue *quality = json_get(root, "quality");
	in->n = json_len(dosage);
	in->dosage = (double *)xmalloc(in->n * sizeof *in->dosage);
	in->depth = (int32_t *)xmalloc(in->n * sizeof *in->depth);
	in->quality = (int32_t *)xmalloc(in->n * sizeof *in->quality);
	for (size_t i = 0; i < in->n; i++) {
		in->dosage[i] = json_num(json_at(dosage, i));
		in->depth[i] = (int32_t)json_int(json_at(depth, i));
		in->quality[i] = (int32_t)json_int(json_at(quality, i));
	}
	in->min_depth = (int32_t)json_int(json_get(root, "min_depth"));
	in->min_quality = (int32_t)json_int(json_get(root, "min_quality"));
}

void input_free(Input *in) {
	free(in->dosage);
	free(in->depth);
	free(in->quality);
	in->dosage = NULL;
	in->depth = NULL;
	in->quality = NULL;
	in->n = 0;
}

Answer solve(const Input *in) {
	const size_t n = in->n;
	const double *dosage = in->dosage;
	const int32_t *depth = in->depth;
	const int32_t *quality = in->quality;

	// Eight samples per step, kept as eight separate running sums: lanes 0-3 in
	// `lo` and 4-7 in `hi`. A lane adds its sample's dosage when both compares
	// keep it and +0.0 when they do not. `kept` counts in integer lanes: a kept
	// sample's mask is -1, so subtracting the mask adds one.
	//
	// Eight sums add the dosages in a different order than one running total.
	// Every partial sum is a multiple of 2^-12 no larger than 2 * 200000 < 2^19,
	// so it needs at most 31 of a double's 53 bits: no add rounds, and the order
	// cannot change the answer.
	const __m256i dmin = _mm256_set1_epi32(in->min_depth - 1);
	const __m256i qmin = _mm256_set1_epi32(in->min_quality - 1);
	__m256d lo = _mm256_setzero_pd();
	__m256d hi = _mm256_setzero_pd();
	__m256i kept = _mm256_setzero_si256();
	size_t i = 0;
	for (; i + 8 <= n; i += 8) {
		const __m256i d = _mm256_loadu_si256((const __m256i *)(depth + i));
		const __m256i q = _mm256_loadu_si256((const __m256i *)(quality + i));
		const __m256i keep = _mm256_and_si256(_mm256_cmpgt_epi32(d, dmin), _mm256_cmpgt_epi32(q, qmin));
		kept = _mm256_sub_epi32(kept, keep);
		const __m256d keep_lo = _mm256_castsi256_pd(_mm256_cvtepi32_epi64(_mm256_castsi256_si128(keep)));
		const __m256d keep_hi = _mm256_castsi256_pd(_mm256_cvtepi32_epi64(_mm256_extracti128_si256(keep, 1)));
		lo = _mm256_add_pd(lo, _mm256_and_pd(keep_lo, _mm256_loadu_pd(dosage + i)));
		hi = _mm256_add_pd(hi, _mm256_and_pd(keep_hi, _mm256_loadu_pd(dosage + i + 4)));
	}

	double lane[8];
	int32_t count[8];
	_mm256_storeu_pd(lane, lo);
	_mm256_storeu_pd(lane + 4, hi);
	_mm256_storeu_si256((__m256i *)count, kept);
	long long passing = 0;
	for (; i < n; i++) {
		if (depth[i] >= in->min_depth && quality[i] >= in->min_quality) {
			lane[0] += dosage[i];
			passing++;
		}
	}
	double ac = 0.0;
	for (int j = 0; j < 8; j++) {
		ac += lane[j];
		passing += count[j];
	}

	Answer a = { ac, 2 * passing };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%.12f %lld\n", a->allele_count, a->called_alleles);
}

void answer_free(Answer *a) {
	(void)a;
}
