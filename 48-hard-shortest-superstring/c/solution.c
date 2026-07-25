#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *reads = json_get(root, "reads");
	in->reads_len = json_len(reads);
	in->reads = (const char **)xmalloc(in->reads_len * sizeof *in->reads);
	for (size_t i = 0; i < in->reads_len; i++) {
		in->reads[i] = json_str(json_at(reads, i));
	}
}

void input_free(Input *in) {
	free(in->reads);
	in->reads = NULL;
	in->reads_len = 0;
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
