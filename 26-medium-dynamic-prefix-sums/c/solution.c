#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));

	const JsonValue *initial = json_get(root, "initial");
	in->initial_len = json_len(initial);
	in->initial = (long long *)xmalloc(in->initial_len * sizeof *in->initial);
	for (size_t i = 0; i < in->initial_len; i++) {
		in->initial[i] = json_int(json_at(initial, i));
	}

	const JsonValue *queries = json_get(root, "queries");
	in->queries_len = json_len(queries);
	in->queries = (Query *)xmalloc(in->queries_len * sizeof *in->queries);
	for (size_t i = 0; i < in->queries_len; i++) {
		const JsonValue *q = json_at(queries, i);
		in->queries[i].kind = json_str(json_at(q, 0));
		in->queries[i].argc = json_len(q) - 1;
		for (size_t k = 0; k < in->queries[i].argc; k++) {
			in->queries[i].arg[k] = json_int(json_at(q, k + 1));
		}
	}
}

void input_free(Input *in) {
	free(in->initial);
	free(in->queries);
	in->initial = NULL;
	in->queries = NULL;
	in->initial_len = 0;
	in->queries_len = 0;
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
