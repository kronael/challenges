#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	int a;
	int b;
} Edge;

typedef struct {
	int n;
	Edge *edges;
	size_t edges_len;
} Input;

typedef struct {
	long long *order;
	size_t n;
	int cycle;
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
