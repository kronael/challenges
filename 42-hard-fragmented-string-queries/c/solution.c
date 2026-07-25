#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *parts = json_get(root, "parts");
	in->parts_len = json_len(parts);
	in->parts = (const char **)xmalloc(in->parts_len * sizeof *in->parts);
	for (size_t i = 0; i < in->parts_len; i++) {
		in->parts[i] = json_str(json_at(parts, i));
	}

	const JsonValue *queries = json_get(root, "queries");
	in->queries_len = json_len(queries);
	in->queries = (Query *)xmalloc(in->queries_len * sizeof *in->queries);
	for (size_t i = 0; i < in->queries_len; i++) {
		const JsonValue *q = json_at(queries, i);
		in->queries[i].lo = json_int(json_at(q, 0));
		in->queries[i].hi = json_int(json_at(q, 1));
	}
}

void input_free(Input *in) {
	free(in->parts);
	free(in->queries);
	in->parts = NULL;
	in->queries = NULL;
	in->parts_len = 0;
	in->queries_len = 0;
}

Answer solve(const Input *in) {
	(void)in;
	return NULL;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%s\n", *a != NULL ? *a : "");
}

void answer_free(Answer *a) {
	free(*a);
	*a = NULL;
}
