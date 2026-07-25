#include "solution.h"

#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	const JsonValue *commands = json_get(root, "commands");
	in->commands_len = json_len(commands);
	in->commands = (Command *)xmalloc(in->commands_len * sizeof *in->commands);
	for (size_t i = 0; i < in->commands_len; i++) {
		const JsonValue *c = json_at(commands, i);
		in->commands[i].operation = json_str(json_at(c, 0));
		in->commands[i].argc = json_len(c) - 1;
		for (size_t k = 0; k < in->commands[i].argc; k++) {
			in->commands[i].arg[k] = json_int(json_at(c, k + 1));
		}
	}
}

void input_free(Input *in) {
	free(in->commands);
	in->commands = NULL;
	in->commands_len = 0;
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
