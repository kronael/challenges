#include "solution.h"

#include <stdlib.h>

static Genome parse_genome(const JsonValue *v) {
	Genome g;
	g.count = json_len(v);
	g.chromosome = (long long **)xmalloc(g.count * sizeof *g.chromosome);
	g.chromosome_len = (size_t *)xmalloc(g.count * sizeof *g.chromosome_len);
	for (size_t i = 0; i < g.count; i++) {
		const JsonValue *chrom = json_at(v, i);
		g.chromosome_len[i] = json_len(chrom);
		g.chromosome[i] =
			(long long *)xmalloc(g.chromosome_len[i] * sizeof *g.chromosome[i]);
		for (size_t k = 0; k < g.chromosome_len[i]; k++) {
			g.chromosome[i][k] = json_int(json_at(chrom, k));
		}
	}
	return g;
}

static void free_genome(Genome *g) {
	for (size_t i = 0; i < g->count; i++) {
		free(g->chromosome[i]);
	}
	free(g->chromosome);
	free(g->chromosome_len);
	g->chromosome = NULL;
	g->chromosome_len = NULL;
	g->count = 0;
}

void input_parse(const JsonValue *root, Input *in) {
	in->a = parse_genome(json_get(root, "a"));
	in->b = parse_genome(json_get(root, "b"));
}

void input_free(Input *in) {
	free_genome(&in->a);
	free_genome(&in->b);
}

Answer solve(const Input *in) {
	(void)in;
	return 0;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld\n", *a);
}

void answer_free(Answer *a) {
	(void)a;
}
