#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	const char *sequence;
	long long *start;
	size_t start_len;
	long long **transition;
	size_t transition_rows;
	size_t transition_cols;
	long long **emission;
	size_t emission_rows;
	size_t emission_cols;
} Input;

typedef struct {
	long long *v;
	size_t n;
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
