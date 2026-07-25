#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->capacity = json_int(json_get(root, "capacity"));
	const JsonValue *items = json_get(root, "items");
	in->items_len = json_len(items);
	in->items = (Item *)xmalloc(in->items_len * sizeof *in->items);
	for (size_t i = 0; i < in->items_len; i++) {
		const JsonValue *it = json_at(items, i);
		in->items[i].weight = json_int(json_get(it, "weight"));
		in->items[i].value = json_int(json_get(it, "value"));
	}
}

void input_free(Input *in) {
	free(in->items);
	in->items = NULL;
	in->items_len = 0;
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
