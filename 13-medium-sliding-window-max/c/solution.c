#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->k = (int)json_int(json_get(root, "k"));
	const JsonValue *arr = json_get(root, "arr");
	in->arr_len = json_len(arr);
	in->arr = (long long *)xmalloc(in->arr_len * sizeof *in->arr);
	for (size_t i = 0; i < in->arr_len; i++) {
		in->arr[i] = json_int(json_at(arr, i));
	}
}

void input_free(Input *in) {
	free(in->arr);
	in->arr = NULL;
	in->arr_len = 0;
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
