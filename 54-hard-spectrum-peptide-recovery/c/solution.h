#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	long long *masses;
	size_t masses_len;
	long long *spectrum;
	size_t spectrum_len;
} Input;

typedef struct {
	long long *v;
	size_t n;
	int ok;
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
