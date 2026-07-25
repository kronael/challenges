#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->rna = json_str(json_get(root, "rna"));
	in->min_loop = (int)json_int(json_get(root, "min_loop"));
	in->allow_wobble = json_bool(json_get(root, "allow_wobble"));
}

void input_free(Input *in) {
	in->rna = NULL;
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
