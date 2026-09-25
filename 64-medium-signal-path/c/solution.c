#include "solution.h"

#include <stdlib.h>

static int *parse_slots(const JsonValue *array, size_t *len) {
	*len = json_len(array);
	int *slots = (int *)xmalloc(*len * sizeof *slots);
	for (size_t i = 0; i < *len; i++) {
		slots[i] = (int)json_int(json_at(array, i));
	}
	return slots;
}

void input_parse(const JsonValue *root, Input *in) {
	in->n = (int)json_int(json_get(root, "n"));
	in->root = (int)json_int(json_get(root, "root"));
	const JsonValue *pnl = json_get(root, "pnl");
	in->pnl_len = json_len(pnl);
	in->pnl = (long long *)xmalloc(in->pnl_len * sizeof *in->pnl);
	for (size_t i = 0; i < in->pnl_len; i++) {
		in->pnl[i] = json_int(json_at(pnl, i));
	}
	in->left = parse_slots(json_get(root, "left"), &in->left_len);
	in->right = parse_slots(json_get(root, "right"), &in->right_len);
}

void input_free(Input *in) {
	free(in->pnl);
	in->pnl = NULL;
	in->pnl_len = 0;
	free(in->left);
	in->left = NULL;
	in->left_len = 0;
	free(in->right);
	in->right = NULL;
	in->right_len = 0;
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
