#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *size = json_get(root, "size");
	const JsonValue *limit = json_get(root, "limit");
	in->size = json_is_null(size) ? 5 : (int)json_int(size);
	in->limit = json_is_null(limit) ? 10000 : (int)json_int(limit);
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
