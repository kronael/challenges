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
	const int32_t qmin = in->min_quality;
	const int32_t dmin = in->min_depth;

	// Reads the samples where they lie: a table of pointers, each record its own
	// allocation. Every iteration loads a pointer, tests it, and only then loads
	// through it, so the compiler has no way to know where sample i+1 sits until
	// it has read sample i's pointer — consecutive samples can never become
	// lanes of one load. Same O(samples) work and the same answer as the
	// reference; the arithmetic just never leaves scalar registers.
	int32_t alt = 0;
	int32_t kept = 0;
	for (size_t i = 0; i < in->n; i++) {
		const Sample *s = in->sample[i];
		if (s == NULL) {
			continue;
		}
		const int32_t keep = (s->quality >= qmin) & (s->depth >= dmin);
		alt += keep * s->genotype;
		kept += keep;
	}

	Answer a = { alt, 2LL * kept };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld %lld\n", a->allele_count, a->called_alleles);
}

void answer_free(Answer *a) {
	(void)a;
}
