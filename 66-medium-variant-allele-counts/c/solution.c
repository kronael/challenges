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
	(void)in;
	Answer a = { 0.0, 0 };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%.12f %lld\n", a->allele_count, a->called_alleles);
}

void answer_free(Answer *a) {
	(void)a;
}
