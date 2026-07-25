#include "solution.h"

#include <stdlib.h>

static Pair *parse_pairs(const JsonValue *arr, size_t *len) {
	*len = json_len(arr);
	Pair *out = (Pair *)xmalloc(*len * sizeof *out);
	for (size_t i = 0; i < *len; i++) {
		const JsonValue *p = json_at(arr, i);
		out[i].a = (int)json_int(json_at(p, 0));
		out[i].b = (int)json_int(json_at(p, 1));
	}
	return out;
}

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	in->unions = parse_pairs(json_get(root, "unions"), &in->unions_len);
	in->queries = parse_pairs(json_get(root, "queries"), &in->queries_len);
}

void input_free(Input *in) {
	free(in->unions);
	free(in->queries);
	in->unions = NULL;
	in->queries = NULL;
	in->unions_len = 0;
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
