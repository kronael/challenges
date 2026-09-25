#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdint.h>
#include <stdio.h>

typedef struct {
	int32_t *score; // one entry per activation, in batch order
	size_t n;
	int32_t threshold;
} Input;

typedef struct {
	int32_t *kept; // the scores above the threshold, in batch order
	size_t n;
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
