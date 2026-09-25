#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *scores = json_get(root, "scores");
	in->n = json_len(scores);
	in->score = (int32_t *)xmalloc(in->n * sizeof *in->score);
	for (size_t i = 0; i < in->n; i++) {
		in->score[i] = (int32_t)json_int(json_at(scores, i));
	}
	in->threshold = (int32_t)json_int(json_get(root, "threshold"));
}

void input_free(Input *in) {
	free(in->score);
	in->score = NULL;
	in->n = 0;
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
		fprintf(out, "%d", a->kept[i]);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	free(a->kept);
	a->kept = NULL;
	a->n = 0;
}
