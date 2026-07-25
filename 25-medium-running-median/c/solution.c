#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *stream = json_get(root, "stream");
	in->stream_len = json_len(stream);
	in->stream = (long long *)xmalloc(in->stream_len * sizeof *in->stream);
	for (size_t i = 0; i < in->stream_len; i++) {
		in->stream[i] = json_int(json_at(stream, i));
	}
}

void input_free(Input *in) {
	free(in->stream);
	in->stream = NULL;
	in->stream_len = 0;
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
		fputs(a->v[i], out);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	for (size_t i = 0; i < a->n; i++) {
		free(a->v[i]);
	}
	free(a->v);
	a->v = NULL;
	a->n = 0;
}
