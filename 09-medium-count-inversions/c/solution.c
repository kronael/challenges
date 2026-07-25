#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
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
	return 0;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld\n", *a);
}

void answer_free(Answer *a) {
	(void)a;
}
