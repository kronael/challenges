#include "solution.h"

#include <stdlib.h>

static long long *read_numbers(const JsonValue *array, size_t *len) {
	*len = json_len(array);
	long long *values = (long long *)xmalloc(*len * sizeof *values);
	for (size_t i = 0; i < *len; i++) {
		values[i] = json_int(json_at(array, i));
	}
	return values;
}

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	in->slippage = read_numbers(json_get(root, "slippage"), &in->slippage_len);
	in->ks = read_numbers(json_get(root, "ks"), &in->ks_len);
}

void input_free(Input *in) {
	free(in->slippage);
	in->slippage = NULL;
	in->slippage_len = 0;
	free(in->ks);
	in->ks = NULL;
	in->ks_len = 0;
}

Answer solve(const Input *in) {
	(void)in;
	Answer a = {NULL, 0};
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
