#include "solution.h"

#include <stdlib.h>

static long long *parse_ints(const JsonValue *arr, size_t *len) {
	*len = json_len(arr);
	long long *out = (long long *)xmalloc(*len * sizeof *out);
	for (size_t i = 0; i < *len; i++) {
		out[i] = json_int(json_at(arr, i));
	}
	return out;
}

void input_parse(const JsonValue *root, Input *in) {
	in->masses = parse_ints(json_get(root, "masses"), &in->masses_len);
	in->spectrum = parse_ints(json_get(root, "spectrum"), &in->spectrum_len);
}

void input_free(Input *in) {
	free(in->masses);
	free(in->spectrum);
	in->masses = NULL;
	in->spectrum = NULL;
	in->masses_len = 0;
	in->spectrum_len = 0;
}

Answer solve(const Input *in) {
	(void)in;
	Answer a = { NULL, 0, 0 };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	if (!a->ok) {
		fprintf(out, "NONE\n");
		return;
	}
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
