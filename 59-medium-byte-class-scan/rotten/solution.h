#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdint.h>
#include <stdio.h>

typedef struct {
	size_t width;       // bytes per frame, terminator included
	size_t *separators; // frame offsets that must hold '|', strictly increasing
	size_t separators_len;
	uint8_t *stream; // the feed as received; a multiple of width bytes
	size_t stream_len;
} Input;

typedef struct {
	long long clean; // frames with no stray byte
	long long stray; // bytes that are not what their offset requires
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
