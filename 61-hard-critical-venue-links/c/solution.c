#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *links = json_get(root, "links");
	in->links_len = json_len(links);
	in->links = (Link *)xmalloc(in->links_len * sizeof *in->links);
	for (size_t i = 0; i < in->links_len; i++) {
		const JsonValue *pair = json_at(links, i);
		in->links[i].u = (int)json_int(json_at(pair, 0));
		in->links[i].v = (int)json_int(json_at(pair, 1));
	}
}

void input_free(Input *in) {
	free(in->links);
	in->links = NULL;
	in->links_len = 0;
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
