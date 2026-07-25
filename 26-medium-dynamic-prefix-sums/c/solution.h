#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	const char *kind;
	long long arg[2];
	size_t argc;
} Query;

typedef struct {
	int n;
	long long *initial;
	size_t initial_len;
	Query *queries;
	size_t queries_len;
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
