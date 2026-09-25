#ifndef SOLUTION_H
#define SOLUTION_H

#include "harness.h"
#include "json.h"

#include <stdint.h>
#include <stdio.h>

typedef struct {
	double *dosage;   // expected alternate alleles per sample, in [0, 2]
	int32_t *depth;   // reads behind each sample's call
	int32_t *quality; // the caller's confidence in each sample's call
	size_t n;
	int32_t min_depth;
	int32_t min_quality;
} Input;

typedef struct {
	double allele_count;      // summed dosage over the passing samples
	long long called_alleles; // two per passing sample
} Answer;

void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);

#endif
