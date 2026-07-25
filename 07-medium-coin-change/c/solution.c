#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->amount = json_int(json_get(root, "amount"));
	const JsonValue *coins = json_get(root, "coins");
	in->coins_len = json_len(coins);
	in->coins = (long long *)xmalloc(in->coins_len * sizeof *in->coins);
	for (size_t i = 0; i < in->coins_len; i++) {
		in->coins[i] = json_int(json_at(coins, i));
	}
}

void input_free(Input *in) {
	free(in->coins);
	in->coins = NULL;
	in->coins_len = 0;
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
