#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));

	const JsonValue *values = json_get(root, "values");
	in->values_len = json_len(values);
	in->values = (long long *)xmalloc(in->values_len * sizeof *in->values);
	for (size_t i = 0; i < in->values_len; i++) {
		in->values[i] = json_int(json_at(values, i));
	}

	const JsonValue *ops = json_get(root, "ops");
	in->ops_len = json_len(ops);
	in->ops = (Op *)xmalloc(in->ops_len * sizeof *in->ops);
	for (size_t i = 0; i < in->ops_len; i++) {
		const JsonValue *o = json_at(ops, i);
		in->ops[i].kind = json_str(json_at(o, 0));
		in->ops[i].a = json_int(json_at(o, 1));
		in->ops[i].b = json_int(json_at(o, 2));
	}
}

void input_free(Input *in) {
	free(in->values);
	free(in->ops);
	in->values = NULL;
	in->ops = NULL;
	in->values_len = 0;
	in->ops_len = 0;
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
