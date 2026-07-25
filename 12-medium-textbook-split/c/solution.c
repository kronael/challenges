#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->k = (int)json_int(json_get(root, "k"));
	const JsonValue *pages = json_get(root, "pages");
	in->pages_len = json_len(pages);
	in->pages = (long long *)xmalloc(in->pages_len * sizeof *in->pages);
	for (size_t i = 0; i < in->pages_len; i++) {
		in->pages[i] = json_int(json_at(pages, i));
	}
}

void input_free(Input *in) {
	free(in->pages);
	in->pages = NULL;
	in->pages_len = 0;
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
