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
	}

	const JsonValue *loads = json_get(root, "loads");
	in->loads_len = json_len(loads);
	in->loads = (long long *)xmalloc(in->loads_len * sizeof *in->loads);
	in->load_given = (int *)xmalloc(in->loads_len * sizeof *in->load_given);
	for (size_t i = 0; i < in->loads_len; i++) {
		const JsonValue *l = json_at(loads, i);
		in->load_given[i] = !json_is_null(l);
		in->loads[i] = in->load_given[i] ? json_int(l) : 0;
	}
}

void input_free(Input *in) {
	free(in->edges);
	free(in->loads);
	free(in->load_given);
	in->edges = NULL;
	in->loads = NULL;
	in->load_given = NULL;
	in->edges_len = 0;
	in->loads_len = 0;
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
