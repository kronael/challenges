#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *samples = json_get(root, "samples");
	in->n = json_len(samples);
	in->sample = (Sample **)xmalloc(in->n * sizeof *in->sample);
	for (size_t i = 0; i < in->n; i++) {
		const JsonValue *entry = json_at(samples, i);
		if (json_is_null(entry)) {
			in->sample[i] = NULL;
			continue;
		}
		Sample *s = (Sample *)xmalloc(sizeof *s);
		s->genotype = (int32_t)json_int(json_get(entry, "genotype"));
		s->depth = (int32_t)json_int(json_get(entry, "depth"));
		s->quality = (int32_t)json_int(json_get(entry, "quality"));
		in->sample[i] = s;
	}
	in->min_depth = (int32_t)json_int(json_get(root, "min_depth"));
	in->min_quality = (int32_t)json_int(json_get(root, "min_quality"));
}

void input_free(Input *in) {
	for (size_t i = 0; i < in->n; i++) {
		free(in->sample[i]);
	}
	free(in->sample);
	in->sample = NULL;
	in->n = 0;
}

Answer solve(const Input *in) {
	(void)in;
	Answer a = { 0, 0 };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld %lld\n", a->allele_count, a->called_alleles);
}

void answer_free(Answer *a) {
	(void)a;
}
