#include "solution.h"

#include <stdlib.h>
#include <string.h>

void input_parse(const JsonValue *root, Input *in) {
	in->k = (int)json_int(json_get(root, "k"));
	const JsonValue *arr = json_get(root, "arr");
	in->arr_len = json_len(arr);
	in->arr = (int32_t *)xmalloc(in->arr_len * sizeof *in->arr);
	for (size_t i = 0; i < in->arr_len; i++) {
		in->arr[i] = (int32_t)json_int(json_at(arr, i));
	}
}

void input_free(Input *in) {
	free(in->arr);
	in->arr = NULL;
	in->arr_len = 0;
}

Answer solve(const Input *in) {
	const size_t n = in->arr_len;
	const size_t k = (size_t)in->k;
	const size_t m = n - k + 1;
	// span[i] is the maximum of the w readings from i. Each pass doubles w,
	// reading span and writing next so the vectorizer has no overlap to check.
	// The window from i is covered by the spans from i and from i + k - w.
	int32_t *span = (int32_t *)xmalloc(n * sizeof *span);
	int32_t *next = (int32_t *)xmalloc(n * sizeof *next);
	memcpy(span, in->arr, n * sizeof *span);
	size_t w = 1;
	for (; 2 * w <= k; w *= 2) {
		for (size_t i = 0; i + 2 * w <= n; i++) {
			next[i] = span[i] > span[i + w] ? span[i] : span[i + w];
		}
		int32_t *swap = span;
		span = next;
		next = swap;
	}
	int32_t *peak = (int32_t *)xmalloc(m * sizeof *peak);
	for (size_t i = 0; i < m; i++) {
		peak[i] = span[i] > span[i + k - w] ? span[i] : span[i + k - w];
	}
	free(span);
	free(next);
	Answer a = {peak, m};
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	for (size_t i = 0; i < a->n; i++) {
		if (i > 0) {
			fputc(' ', out);
		}
		fprintf(out, "%d", a->v[i]);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	free(a->v);
	a->v = NULL;
	a->n = 0;
}
