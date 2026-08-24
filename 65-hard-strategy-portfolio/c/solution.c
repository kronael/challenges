#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	const JsonValue *pnl = json_get(root, "pnl");
	in->pnl_len = json_len(pnl);
	in->pnl = (long long *)xmalloc(in->pnl_len * sizeof *in->pnl);
	for (size_t i = 0; i < in->pnl_len; i++) {
		in->pnl[i] = json_int(json_at(pnl, i));
	}
	const JsonValue *pairs = json_get(root, "requires");
	in->reqs_len = json_len(pairs);
	in->reqs = (Requirement *)xmalloc(in->reqs_len * sizeof *in->reqs);
	for (size_t i = 0; i < in->reqs_len; i++) {
		const JsonValue *pair = json_at(pairs, i);
		in->reqs[i].a = (int)json_int(json_at(pair, 0));
		in->reqs[i].b = (int)json_int(json_at(pair, 1));
	}
}

void input_free(Input *in) {
	free(in->pnl);
	in->pnl = NULL;
	in->pnl_len = 0;
	free(in->reqs);
	in->reqs = NULL;
	in->reqs_len = 0;
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
