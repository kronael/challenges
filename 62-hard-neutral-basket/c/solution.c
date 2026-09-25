#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	in->target = json_int(json_get(root, "target"));
	const JsonValue *exposures = json_get(root, "exposures");
	in->exposures_len = json_len(exposures);
	in->exposures = (long long *)xmalloc(in->exposures_len * sizeof *in->exposures);
	for (size_t i = 0; i < in->exposures_len; i++) {
		in->exposures[i] = json_int(json_at(exposures, i));
	}
}

void input_free(Input *in) {
	free(in->exposures);
	in->exposures = NULL;
	in->exposures_len = 0;
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
