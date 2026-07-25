#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *jobs = json_get(root, "jobs");
	in->jobs_len = json_len(jobs);
	in->jobs = (Job *)xmalloc(in->jobs_len * sizeof *in->jobs);
	for (size_t i = 0; i < in->jobs_len; i++) {
		const JsonValue *j = json_at(jobs, i);
		in->jobs[i].start = json_int(json_get(j, "start"));
		in->jobs[i].end = json_int(json_get(j, "end"));
		in->jobs[i].weight = json_int(json_get(j, "weight"));
	}
}

void input_free(Input *in) {
	free(in->jobs);
	in->jobs = NULL;
	in->jobs_len = 0;
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
