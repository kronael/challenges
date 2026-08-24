#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *quantities = json_get(root, "quantities");
	in->quantities_len = json_len(quantities);
	in->quantities = (long long *)xmalloc(in->quantities_len * sizeof *in->quantities);
	for (size_t i = 0; i < in->quantities_len; i++) {
		in->quantities[i] = json_int(json_at(quantities, i));
	}
}

void input_free(Input *in) {
	free(in->quantities);
	in->quantities = NULL;
	in->quantities_len = 0;
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
