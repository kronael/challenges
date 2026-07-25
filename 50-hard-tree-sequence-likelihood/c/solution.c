#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *parent = json_get(root, "parent");
	in->parent_len = json_len(parent);
	in->parent = (long long *)xmalloc(in->parent_len * sizeof *in->parent);
	for (size_t i = 0; i < in->parent_len; i++) {
		in->parent[i] = json_int(json_at(parent, i));
	}

	// A null sequence marks an internal node with no observed bases.
	const JsonValue *sequences = json_get(root, "sequences");
	in->sequences_len = json_len(sequences);
	in->sequences = (const char **)xmalloc(in->sequences_len * sizeof *in->sequences);
	for (size_t i = 0; i < in->sequences_len; i++) {
		const JsonValue *s = json_at(sequences, i);
		in->sequences[i] = json_is_null(s) ? NULL : json_str(s);
	}

	const JsonValue *prior = json_get(root, "prior");
	in->prior_len = json_len(prior);
	in->prior = (double *)xmalloc(in->prior_len * sizeof *in->prior);
	for (size_t i = 0; i < in->prior_len; i++) {
		in->prior[i] = json_num(json_at(prior, i));
	}

	const JsonValue *transition = json_get(root, "transition");
	in->transition_rows = json_len(transition);
	in->transition = (double **)xmalloc(in->transition_rows * sizeof *in->transition);
	for (size_t r = 0; r < in->transition_rows; r++) {
		const JsonValue *row = json_at(transition, r);
		size_t cols = json_len(row);
		in->transition[r] = (double *)xmalloc(cols * sizeof *in->transition[r]);
		for (size_t c = 0; c < cols; c++) {
			in->transition[r][c] = json_num(json_at(row, c));
		}
	}
}

void input_free(Input *in) {
	free(in->parent);
	free(in->sequences);
	free(in->prior);
	for (size_t r = 0; r < in->transition_rows; r++) {
		free(in->transition[r]);
	}
	free(in->transition);
	in->parent = NULL;
	in->sequences = NULL;
	in->prior = NULL;
	in->transition = NULL;
	in->parent_len = 0;
	in->sequences_len = 0;
	in->prior_len = 0;
	in->transition_rows = 0;
}

Answer solve(const Input *in) {
	(void)in;
	return 0.0;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%.6f\n", *a);
}

void answer_free(Answer *a) {
	(void)a;
}
