#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *intervals = json_get(root, "intervals");
	in->intervals_len = json_len(intervals);
	in->intervals = (Interval *)xmalloc(in->intervals_len * sizeof *in->intervals);
	for (size_t i = 0; i < in->intervals_len; i++) {
		const JsonValue *iv = json_at(intervals, i);
		in->intervals[i].start = json_int(json_at(iv, 0));
		in->intervals[i].end = json_int(json_at(iv, 1));
	}
}

void input_free(Input *in) {
	free(in->intervals);
	in->intervals = NULL;
	in->intervals_len = 0;
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
