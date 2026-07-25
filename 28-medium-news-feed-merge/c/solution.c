#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *feeds = json_get(root, "feeds");
	in->feeds_len = json_len(feeds);
	in->feeds = (Event **)xmalloc(in->feeds_len * sizeof *in->feeds);
	in->feed_len = (size_t *)xmalloc(in->feeds_len * sizeof *in->feed_len);
	for (size_t f = 0; f < in->feeds_len; f++) {
		const JsonValue *feed = json_at(feeds, f);
		in->feed_len[f] = json_len(feed);
		in->feeds[f] = (Event *)xmalloc(in->feed_len[f] * sizeof *in->feeds[f]);
		for (size_t i = 0; i < in->feed_len[f]; i++) {
			const JsonValue *e = json_at(feed, i);
			in->feeds[f][i].ts = json_int(json_get(e, "ts"));
			in->feeds[f][i].id = json_int(json_get(e, "id"));
		}
	}
}

void input_free(Input *in) {
	for (size_t f = 0; f < in->feeds_len; f++) {
		free(in->feeds[f]);
	}
	free(in->feeds);
	free(in->feed_len);
	in->feeds = NULL;
	in->feed_len = NULL;
	in->feeds_len = 0;
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
