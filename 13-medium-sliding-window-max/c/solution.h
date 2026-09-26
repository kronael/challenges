#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdint.h>
#include <stdio.h>

typedef struct {
	int k;
	int32_t *arr;
	size_t arr_len;
} Input;

typedef struct {
	int32_t *v;
	size_t n;
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
