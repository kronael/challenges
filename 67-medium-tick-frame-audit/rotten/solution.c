#include "solution.h"

#include <stdlib.h>
#include <string.h>

enum { PAYLOAD, SEPARATOR, TERMINATOR };

void input_parse(const JsonValue *root, Input *in) {
	in->width = (size_t)json_int(json_get(root, "width"));
	const JsonValue *separators = json_get(root, "separators");
	in->separators_len = json_len(separators);
	in->separators = (size_t *)xmalloc(in->separators_len * sizeof *in->separators);
	for (size_t i = 0; i < in->separators_len; i++) {
		in->separators[i] = (size_t)json_int(json_at(separators, i));
	}
	const char *stream = json_str(json_get(root, "stream"));
	in->stream_len = strlen(stream);
	in->stream = (uint8_t *)xmalloc(in->stream_len);
	memcpy(in->stream, stream, in->stream_len);
}

void input_free(Input *in) {
	free(in->separators);
	free(in->stream);
	in->separators = NULL;
	in->stream = NULL;
	in->separators_len = 0;
	in->stream_len = 0;
}

Answer solve(const Input *in) {
	const size_t w = in->width;

	uint8_t *expect = (uint8_t *)xcalloc(w, sizeof *expect);
	for (size_t k = 0; k < in->separators_len; k++) {
		expect[in->separators[k]] = SEPARATOR;
	}
	expect[w - 1] = TERMINATOR;

	// The handler's first draft: one cursor walks the feed, a switch names each
	// byte, and `pos` wraps back to 0 at the frame edge. Each of the two keeps
	// the loop in scalar registers on its own: gcc 12 does not if-convert a
	// switch ("control flow in loop"), and `pos` depends on the previous
	// iteration's `pos` rather than on `i`, so `expect[pos]` is not a
	// unit-stride read ("not suitable for gather load"). Same O(bytes) work
	// and the same answer as the reference.
	long long clean = 0;
	long long stray = 0;
	size_t pos = 0;
	int bad = 0;
	for (size_t i = 0; i < in->stream_len; i++) {
		uint8_t cls;
		switch (in->stream[i]) {
		case '|':
			cls = SEPARATOR;
			break;
		case '\n':
			cls = TERMINATOR;
			break;
		default:
			cls = PAYLOAD;
			break;
		}
		if (cls != expect[pos]) {
			stray++;
			bad = 1;
		}
		if (++pos == w) {
			clean += !bad;
			bad = 0;
			pos = 0;
		}
	}

	free(expect);

	Answer a = { clean, stray };
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld %lld\n", a->clean, a->stray);
}

void answer_free(Answer *a) {
	(void)a;
}
