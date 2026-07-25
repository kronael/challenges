#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->k = (int)json_int(json_get(root, "k"));
	const JsonValue *kmers = json_get(root, "kmers");
	in->kmers_len = json_len(kmers);
	in->kmers = (const char **)xmalloc(in->kmers_len * sizeof *in->kmers);
	for (size_t i = 0; i < in->kmers_len; i++) {
		in->kmers[i] = json_str(json_at(kmers, i));
	}
}

void input_free(Input *in) {
	free(in->kmers);
	in->kmers = NULL;
	in->kmers_len = 0;
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
