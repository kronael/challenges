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
	return 0;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld\n", *a);
}

void answer_free(Answer *a) {
	(void)a;
}
