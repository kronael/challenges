#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdint.h>
#include <stdio.h>

typedef struct {
	int32_t genotype;
	int32_t depth;
	int32_t quality;
} Sample;

typedef struct {
	Sample **sample; // one entry per sample; NULL where there is no call
	size_t n;
	int32_t min_depth;
	int32_t min_quality;
} Input;

typedef struct {
	long long allele_count;   // alternate alleles over the passing samples
	long long called_alleles; // two per passing sample
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
