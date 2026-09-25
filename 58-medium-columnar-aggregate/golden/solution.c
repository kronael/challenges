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
	const size_t n = in->n;
	const int32_t qmin = in->min_quality;
	const int32_t dmin = in->min_depth;

	// One pass copies the called samples out of their separate records into an
	// array per field, dropping the absent ones on the way.
	int32_t *genotype = (int32_t *)xmalloc(n * sizeof *genotype);
	int32_t *depth = (int32_t *)xmalloc(n * sizeof *depth);
	int32_t *quality = (int32_t *)xmalloc(n * sizeof *quality);
	size_t called = 0;
	for (size_t i = 0; i < n; i++) {
		const Sample *s = in->sample[i];
		if (s == NULL) {
			continue;
		}
		genotype[called] = s->genotype;
		depth[called] = s->depth;
		quality[called] = s->quality;
		called++;
	}

	// Both thresholds and both running totals now read unit-stride streams, so
	// consecutive samples are lanes of one vector and no operand needs a scalar
	// register. `keep` is 0 or 1, which turns the filter into a multiply.
	int32_t alt = 0;
	int32_t kept = 0;
	for (size_t i = 0; i < called; i++) {
		const int32_t keep = (quality[i] >= qmin) & (depth[i] >= dmin);
		alt += keep * genotype[i];
		kept += keep;
	}

	free(quality);
	free(depth);
	free(genotype);

	Answer a = { alt, 2LL * kept };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld %lld\n", a->allele_count, a->called_alleles);
}

void answer_free(Answer *a) {
	(void)a;
}
