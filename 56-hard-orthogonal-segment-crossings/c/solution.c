#include "solution.h"

#include <stdlib.h>

static Segment *parse_segments(const JsonValue *arr, size_t *len) {
	*len = json_len(arr);
	Segment *out = (Segment *)xmalloc(*len * sizeof *out);
	for (size_t i = 0; i < *len; i++) {
		const JsonValue *s = json_at(arr, i);
		for (size_t k = 0; k < 3; k++) {
			out[i].p[k] = json_int(json_at(s, k));
		}
	}
	return out;
}

void input_parse(const JsonValue *root, Input *in) {
	in->horizontal = parse_segments(json_get(root, "horizontal"), &in->horizontal_len);
	in->vertical = parse_segments(json_get(root, "vertical"), &in->vertical_len);
}

void input_free(Input *in) {
	free(in->horizontal);
	free(in->vertical);
	in->horizontal = NULL;
	in->vertical = NULL;
	in->horizontal_len = 0;
	in->vertical_len = 0;
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
