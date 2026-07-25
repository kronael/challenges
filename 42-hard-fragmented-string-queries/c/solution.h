#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	long long lo;
	long long hi;
} Query;

typedef struct {
	const char **parts;
	size_t parts_len;
	Query *queries;
	size_t queries_len;
} Input;

typedef char *Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
