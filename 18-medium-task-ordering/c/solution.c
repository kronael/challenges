#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *edges = json_get(root, "edges");
	in->edges_len = json_len(edges);
	in->edges = (Edge *)xmalloc(in->edges_len * sizeof *in->edges);
	for (size_t i = 0; i < in->edges_len; i++) {
		const JsonValue *e = json_at(edges, i);
		in->edges[i].a = (int)json_int(json_at(e, 0));
		in->edges[i].b = (int)json_int(json_at(e, 1));
	}
}

void input_free(Input *in) {
	free(in->edges);
	in->edges = NULL;
	in->edges_len = 0;
}

Answer solve(const Input *in) {
	(void)in;
	Answer a = { NULL, 0, 0 };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	if (a->cycle) {
		fprintf(out, "CYCLE\n");
		return;
	}
	for (size_t i = 0; i < a->n; i++) {
		if (i > 0) {
			fputc(' ', out);
		}
		fprintf(out, "%lld", a->order[i]);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	free(a->order);
	a->order = NULL;
	a->n = 0;
}
