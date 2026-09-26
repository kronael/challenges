#include "solution.h"

#include <stdlib.h>
#include <string.h>

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
	// Each item reads the row best and writes next, so the vectorizer has no
	// overlap to check. Budgets below the item's weight copy across.
	const size_t cap = (size_t)in->capacity;
	long long *best = (long long *)xcalloc(cap + 1, sizeof *best);
	long long *next = (long long *)xmalloc((cap + 1) * sizeof *next);
	for (size_t i = 0; i < in->items_len; i++) {
		if (in->items[i].weight > in->capacity) {
			continue;
		}
		const size_t w = (size_t)in->items[i].weight;
		const long long v = in->items[i].value;
		memcpy(next, best, w * sizeof *next);
		for (size_t c = w; c <= cap; c++) {
			const long long take = best[c - w] + v;
			next[c] = take > best[c] ? take : best[c];
		}
		long long *swap = best;
		best = next;
		next = swap;
	}
	const Answer a = best[cap];
	free(best);
	free(next);
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld\n", *a);
}

void answer_free(Answer *a) {
	(void)a;
}
