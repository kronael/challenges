#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *prices = json_get(root, "prices");
	in->prices_len = json_len(prices);
	in->prices = (long long *)xmalloc(in->prices_len * sizeof *in->prices);
	for (size_t i = 0; i < in->prices_len; i++) {
		in->prices[i] = json_int(json_at(prices, i));
	}
}

void input_free(Input *in) {
	free(in->prices);
	in->prices = NULL;
	in->prices_len = 0;
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
