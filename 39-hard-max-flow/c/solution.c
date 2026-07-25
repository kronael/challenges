#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *edges = json_get(root, "edges");
	in->edges_len = json_len(edges);
	in->edges = (Edge *)xmalloc(in->edges_len * sizeof *in->edges);
	for (size_t i = 0; i < in->edges_len; i++) {
		const JsonValue *e = json_at(edges, i);
		in->edges[i].u = (int)json_int(json_at(e, 0));
		in->edges[i].v = (int)json_int(json_at(e, 1));
		in->edges[i].c = json_int(json_at(e, 2));
	}
}

void input_free(Input *in) {
	free(in->edges);
	in->edges = NULL;
	in->edges_len = 0;
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
