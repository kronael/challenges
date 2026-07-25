#include "solution.h"

#include <stdlib.h>

static const char **parse_strings(const JsonValue *arr, size_t *len) {
	*len = json_len(arr);
	const char **out = (const char **)xmalloc(*len * sizeof *out);
	for (size_t i = 0; i < *len; i++) {
		out[i] = json_str(json_at(arr, i));
	}
	return out;
}

void input_parse(const JsonValue *root, Input *in) {
	in->words = parse_strings(json_get(root, "words"), &in->words_len);
	in->queries = parse_strings(json_get(root, "queries"), &in->queries_len);
}

void input_free(Input *in) {
	free(in->words);
	free(in->queries);
	in->words = NULL;
	in->queries = NULL;
	in->words_len = 0;
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
