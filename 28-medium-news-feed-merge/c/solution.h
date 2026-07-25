#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdio.h>

typedef struct {
	long long ts;
	long long id;
} Event;

typedef struct {
	Event **feeds;
	size_t *feed_len;
	size_t feeds_len;
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
