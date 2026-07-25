#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *orders = json_get(root, "orders");
	in->orders_len = json_len(orders);
	in->orders = (Order *)xmalloc(in->orders_len * sizeof *in->orders);
	for (size_t i = 0; i < in->orders_len; i++) {
		const JsonValue *o = json_at(orders, i);
		in->orders[i].side = json_str(json_get(o, "side"));
		in->orders[i].price = json_int(json_get(o, "price"));
		in->orders[i].qty = json_int(json_get(o, "qty"));
		in->orders[i].type = json_str(json_get(o, "type"));
	}
}

void input_free(Input *in) {
	free(in->orders);
	in->orders = NULL;
	in->orders_len = 0;
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
		fprintf(out, "%lld", a->v[i]);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	free(a->v);
	a->v = NULL;
	a->n = 0;
}
