#include "solution.h"

#include <stdlib.h>

static long long **parse_matrix(const JsonValue *m, size_t *rows, size_t *cols) {
	*rows = json_len(m);
	*cols = *rows > 0 ? json_len(json_at(m, 0)) : 0;
	long long **out = (long long **)xmalloc(*rows * sizeof *out);
	for (size_t r = 0; r < *rows; r++) {
		const JsonValue *row = json_at(m, r);
		out[r] = (long long *)xmalloc(json_len(row) * sizeof *out[r]);
		for (size_t c = 0; c < json_len(row); c++) {
			out[r][c] = json_int(json_at(row, c));
		}
	}
	return out;
}

static void free_matrix(long long **m, size_t rows) {
	for (size_t r = 0; r < rows; r++) {
		free(m[r]);
	}
	free(m);
}

void input_parse(const JsonValue *root, Input *in) {
	in->sequence = json_str(json_get(root, "sequence"));

	const JsonValue *start = json_get(root, "start");
	in->start_len = json_len(start);
	in->start = (long long *)xmalloc(in->start_len * sizeof *in->start);
	for (size_t i = 0; i < in->start_len; i++) {
		in->start[i] = json_int(json_at(start, i));
	}

	in->transition = parse_matrix(json_get(root, "transition"), &in->transition_rows,
				      &in->transition_cols);
	in->emission =
		parse_matrix(json_get(root, "emission"), &in->emission_rows, &in->emission_cols);
}

void input_free(Input *in) {
	free(in->start);
	free_matrix(in->transition, in->transition_rows);
	free_matrix(in->emission, in->emission_rows);
	in->start = NULL;
	in->transition = NULL;
	in->emission = NULL;
	in->start_len = 0;
	in->transition_rows = 0;
	in->emission_rows = 0;
}

Answer solve(const Input *in) {
	(void)in;
	Answer a = { NULL, 0 };
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
