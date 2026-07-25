#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	long long **chromosome;
	size_t *chromosome_len;
	size_t count;
} Genome;

typedef struct {
	Genome a;
	Genome b;
} Input;

typedef long long Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
