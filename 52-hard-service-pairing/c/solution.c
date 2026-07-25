#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *costs = json_get(root, "costs");
	in->rows = json_len(costs);
	in->cols = in->rows > 0 ? json_len(json_at(costs, 0)) : 0;
	in->costs = (long long **)xmalloc(in->rows * sizeof *in->costs);
	for (size_t r = 0; r < in->rows; r++) {
		const JsonValue *row = json_at(costs, r);
		in->costs[r] = (long long *)xmalloc(json_len(row) * sizeof *in->costs[r]);
		for (size_t c = 0; c < json_len(row); c++) {
			in->costs[r][c] = json_int(json_at(row, c));
		}
	}
}

void input_free(Input *in) {
	for (size_t r = 0; r < in->rows; r++) {
		free(in->costs[r]);
	}
	free(in->costs);
	in->costs = NULL;
	in->rows = 0;
	in->cols = 0;
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
