#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->s = json_str(json_get(root, "s"));
	in->t = json_str(json_get(root, "t"));
}

void input_free(Input *in) {
	in->s = NULL;
	in->t = NULL;
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
