#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->d = (int)json_int(json_get(root, "d"));
	in->len = (int)json_int(json_get(root, "len"));
	in->genome = json_str(json_get(root, "genome"));
	const JsonValue *guides = json_get(root, "guides");
	in->guides_len = json_len(guides);
	in->guides = (const char **)xmalloc(in->guides_len * sizeof *in->guides);
	for (size_t i = 0; i < in->guides_len; i++) {
		in->guides[i] = json_str(json_at(guides, i));
	}
}

void input_free(Input *in) {
	free(in->guides);
	in->guides = NULL;
	in->guides_len = 0;
	in->genome = NULL;
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
