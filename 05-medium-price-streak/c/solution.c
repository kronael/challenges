#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *seq = json_get(root, "seq");
	in->seq_len = json_len(seq);
	in->seq = (long long *)xmalloc(in->seq_len * sizeof *in->seq);
	for (size_t i = 0; i < in->seq_len; i++) {
		in->seq[i] = json_int(json_at(seq, i));
	}
}

void input_free(Input *in) {
	free(in->seq);
	in->seq = NULL;
	in->seq_len = 0;
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
