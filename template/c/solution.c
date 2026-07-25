#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *data = json_get(root, "data");
	in->data_len = json_len(data);
	in->data = (long long *)xmalloc(in->data_len * sizeof *in->data);
	for (size_t i = 0; i < in->data_len; i++) {
		in->data[i] = json_int(json_at(data, i));
	}
}

void input_free(Input *in) {
	free(in->data);
	in->data = NULL;
	in->data_len = 0;
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
