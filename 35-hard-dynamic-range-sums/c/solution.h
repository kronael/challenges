#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	const char *kind;
	long long a;
	long long b;
} Op;

typedef struct {
	int n;
	long long *values;
	size_t values_len;
	Op *ops;
	size_t ops_len;
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
