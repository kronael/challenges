#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *parent = json_get(root, "parent");
	in->parent_len = json_len(parent);
	in->parent = (int *)xmalloc(in->parent_len * sizeof *in->parent);
	for (size_t i = 0; i < in->parent_len; i++) {
		in->parent[i] = (int)json_int(json_at(parent, i));
	}
	const JsonValue *queries = json_get(root, "queries");
	in->queries_len = json_len(queries);
	in->queries = (Query *)xmalloc(in->queries_len * sizeof *in->queries);
	for (size_t i = 0; i < in->queries_len; i++) {
		const JsonValue *pair = json_at(queries, i);
		in->queries[i].a = (int)json_int(json_at(pair, 0));
		in->queries[i].b = (int)json_int(json_at(pair, 1));
	}
}

void input_free(Input *in) {
	free(in->parent);
	in->parent = NULL;
	in->parent_len = 0;
	free(in->queries);
	in->queries = NULL;
	in->queries_len = 0;
}

Answer solve(const Input *in) {
	(void)in;
	Answer a = {NULL, 0};
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
