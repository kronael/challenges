#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *ops = json_get(root, "ops");
	in->ops_len = json_len(ops);
	in->ops = (Op *)xmalloc(in->ops_len * sizeof *in->ops);
	for (size_t i = 0; i < in->ops_len; i++) {
		const JsonValue *o = json_at(ops, i);
		in->ops[i].kind = json_str(json_at(o, 0));
		in->ops[i].argc = json_len(o) - 1;
		for (size_t k = 0; k < in->ops[i].argc; k++) {
			in->ops[i].arg[k] = json_int(json_at(o, k + 1));
		}
	}
}

void input_free(Input *in) {
	free(in->ops);
	in->ops = NULL;
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
