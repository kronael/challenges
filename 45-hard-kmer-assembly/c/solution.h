#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	int k;
	const char **kmers;
	size_t kmers_len;
} Input;

typedef char *Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
