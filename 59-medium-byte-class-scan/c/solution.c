#include "solution.h"

#include <stdlib.h>
#include <string.h>

void input_parse(const JsonValue *root, Input *in) {
	in->width = (size_t)json_int(json_get(root, "width"));
	const JsonValue *separators = json_get(root, "separators");
	in->separators_len = json_len(separators);
	in->separators = (size_t *)xmalloc(in->separators_len * sizeof *in->separators);
	for (size_t i = 0; i < in->separators_len; i++) {
		in->separators[i] = (size_t)json_int(json_at(separators, i));
	}
	const char *stream = json_str(json_get(root, "stream"));
	in->stream_len = strlen(stream);
	in->stream = (uint8_t *)xmalloc(in->stream_len);
	memcpy(in->stream, stream, in->stream_len);
}

void input_free(Input *in) {
	free(in->separators);
	free(in->stream);
	in->separators = NULL;
	in->stream = NULL;
	in->separators_len = 0;
	in->stream_len = 0;
}

Answer solve(const Input *in) {
	(void)in;
	Answer a = { 0, 0 };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld %lld\n", a->clean, a->stray);
}

void answer_free(Answer *a) {
	(void)a;
}
