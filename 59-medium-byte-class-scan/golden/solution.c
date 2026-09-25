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
	const size_t frames = in->stream_len / w;

	// The class every offset of a frame must hold, laid out once, so that a
	// frame's bytes and their required classes are two unit-stride streams.
	uint8_t *expect = (uint8_t *)xcalloc(w, sizeof *expect);
	for (size_t k = 0; k < in->separators_len; k++) {
		expect[in->separators[k]] = SEPARATOR;
	}
	expect[w - 1] = TERMINATOR;

	// Frame by frame. The offset is the inner induction variable rather than a
	// cursor carried from the previous byte, and a byte's class is arithmetic on
	// two compares, so consecutive bytes are lanes of one vector compare and the
	// mismatch count is a widening sum with no branch in it.
	long long clean = 0;
	long long stray = 0;
	for (size_t f = 0; f < frames; f++) {
		const uint8_t *rec = in->stream + f * w;
		uint32_t mism = 0;
		for (size_t j = 0; j < w; j++) {
			const uint8_t cls = (rec[j] == '|') * SEPARATOR + (rec[j] == '\n') * TERMINATOR;
			mism += cls != expect[j];
		}
		stray += mism;
		clean += mism == 0;
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
