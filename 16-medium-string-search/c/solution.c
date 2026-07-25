#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->text = json_str(json_get(root, "text"));
	in->pattern = json_str(json_get(root, "pattern"));
}

void input_free(Input *in) {
	in->text = NULL;
	in->pattern = NULL;
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
