#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *scores = json_get(root, "scores");
	in->n = json_len(scores);
	in->scores = (int32_t *)xmalloc(in->n * sizeof *in->scores);
	for (size_t i = 0; i < in->n; i++) {
		in->scores[i] = (int32_t)json_int(json_at(scores, i));
	}
	in->threshold = (int32_t)json_int(json_get(root, "threshold"));
}

void input_free(Input *in) {
	free(in->scores);
	in->scores = NULL;
	in->n = 0;
}

Answer solve(const Input *in) {
	int32_t *kept = (int32_t *)xmalloc(in->n * sizeof *kept);
	size_t k = 0;

	// Appends each score that clears the threshold at the next free slot. Where
	// score i lands depends on how many of scores 0..i-1 were kept, so lane i+1
	// cannot pick its address until lane i has decided: the store index is a
	// loop-carried dependency and gcc reports the loop as `not vectorized:
	// unsupported use in stmt`. Same O(n) work and the same answer as the
	// reference; the selection just never leaves scalar registers.
	for (size_t i = 0; i < in->n; i++) {
		if (in->scores[i] > in->threshold) {
			kept[k++] = in->scores[i];
		}
	}

	Answer a = {kept, k};
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
