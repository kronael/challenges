#include "solution.h"

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
	// One running total, added to in sample order. Floating-point addition is
	// not associative, so without -ffast-math the compiler has to perform the
	// adds in exactly this order: each waits on the sum the previous one
	// produced, and gcc and clang both keep the loop in scalar registers at any
	// -mtune. Same O(samples) work and the same answer as the reference.
	double ac = 0.0;
	long long kept = 0;
	for (size_t i = 0; i < in->n; i++) {
		if (in->depth[i] >= in->min_depth && in->quality[i] >= in->min_quality) {
			ac += in->dosage[i];
			kept++;
		}
	}

	Answer a = { ac, 2 * kept };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%.12f %lld\n", a->allele_count, a->called_alleles);
}

void answer_free(Answer *a) {
	(void)a;
}
