#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

#define GAP_OPEN 11
#define GAP_EXTEND 1

extern const char AA[21];
extern const int BLOSUM62[20][20];

int aa_index(char c);

typedef struct {
	const char *s;
	const char *t;
} Input;

typedef long long Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
