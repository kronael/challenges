#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *operations = json_get(root, "operations");
	in->operations_len = json_len(operations);
	in->operations = (Operation *)xmalloc(in->operations_len * sizeof *in->operations);
	for (size_t i = 0; i < in->operations_len; i++) {
		const JsonValue *o = json_at(operations, i);
		in->operations[i].type = json_str(json_get(o, "type"));
		in->operations[i].u = (int)json_int(json_get(o, "u"));
		in->operations[i].v = (int)json_int(json_get(o, "v"));
	}
}

void input_free(Input *in) {
	free(in->operations);
	in->operations = NULL;
	in->operations_len = 0;
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
