#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *dims = json_get(root, "dims");
	in->dims_len = json_len(dims);
	in->dims = (long long *)xmalloc(in->dims_len * sizeof *in->dims);
	for (size_t i = 0; i < in->dims_len; i++) {
		in->dims[i] = json_int(json_at(dims, i));
	}
}

void input_free(Input *in) {
	free(in->dims);
	in->dims = NULL;
	in->dims_len = 0;
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
