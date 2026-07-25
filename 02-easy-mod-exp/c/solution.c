#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->base = json_int(json_get(root, "base"));
	in->exp = json_int(json_get(root, "exp"));
	in->mod = json_int(json_get(root, "mod"));
}

void input_free(Input *in) {
	(void)in;
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
