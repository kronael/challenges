#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	long long *parent;
	size_t parent_len;
	const char **sequences;
	size_t sequences_len;
	double *prior;
	size_t prior_len;
	double **transition;
	size_t transition_rows;
} Input;

typedef double Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
