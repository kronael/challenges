#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->processes = (int)json_int(json_get(root, "processes"));
	const JsonValue *events = json_get(root, "events");
	in->events_len = json_len(events);
	in->events = (Event *)xmalloc(in->events_len * sizeof *in->events);
	for (size_t i = 0; i < in->events_len; i++) {
		const JsonValue *e = json_at(events, i);
		in->events[i].id = (int)json_int(json_get(e, "id"));
		in->events[i].process = (int)json_int(json_get(e, "process"));
		const JsonValue *clock = json_get(e, "clock");
		in->events[i].clock_len = json_len(clock);
		in->events[i].clock = (long long *)xmalloc(in->events[i].clock_len *
							   sizeof *in->events[i].clock);
		for (size_t k = 0; k < in->events[i].clock_len; k++) {
			in->events[i].clock[k] = json_int(json_at(clock, k));
		}
	}
}

void input_free(Input *in) {
	for (size_t i = 0; i < in->events_len; i++) {
		free(in->events[i].clock);
	}
	free(in->events);
	in->events = NULL;
	in->events_len = 0;
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
