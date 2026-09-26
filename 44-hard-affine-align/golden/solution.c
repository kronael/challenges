#include "solution.h"

#include <immintrin.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

const char AA[21] = "ARNDCQEGHILKMFPSTWYV";

// BLOSUM62 substitution scores, rows/cols in AA order.
const int BLOSUM62[20][20] = {
    {4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, -3, -2, 0},
    {-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -2, -3},
    {-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -4, -2, -3},
    {-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -4, -3, -3},
    {0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1},
    {-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2},
    {-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -3, -2, -2},
    {0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3},
    {-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, 2, -3},
    {-1, -3, -3, -3, -1, -3, -3, -4, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, 3},
    {-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -1, -2, -1, 1},
    {-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -1, -3, -1, 0, -1, -3, -2, -2},
    {-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -1, 5, 0, -2, -1, -1, -1, -1, 1},
    {-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 0, 6, -4, -2, -2, 1, 3, -1},
    {-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2},
    {1, -1, 1, 0, -1, 0, 0, 0, -1, -2, -2, 0, -1, -2, -1, 4, 1, -3, -2, -2},
    {0, -1, 0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1, 5, -2, -2, 0},
    {-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1, -4, -3, -2, 11, 2, -3},
    {-2, -2, -2, -3, -2, -1, -2, -3, 2, -1, -1, -2, -1, 3, -3, -2, -2, 2, 7, -1},
    {0, -3, -3, -3, -1, -2, -2, -3, -3, 3, 1, -2, 1, -1, -2, -2, 0, -3, -1, 4},
};

// Index of an amino acid in the AA / BLOSUM62 ordering.
int aa_index(char c) {
	const char *hit = strchr(AA, c);
	if (hit == NULL || c == '\0') {
		fprintf(stderr, "not an amino acid: %c\n", c);
		exit(1);
	}
	return (int)(hit - AA);
}

void input_parse(const JsonValue *root, Input *in) {
	in->s = json_str(json_get(root, "s"));
	in->t = json_str(json_get(root, "t"));
}

void input_free(Input *in) {
	in->s = NULL;
	in->t = NULL;
}

// Sixteen 16-bit scores per vector. For |s|, |t| <= 2000 every score a cell can
// hold lies within ±22000, so 16 bits suffice, and saturating arithmetic keeps
// the minus-infinity sentinel from wrapping around.
enum { LANES = 16 };
#define NEG INT16_MIN

// Moves lane k to lane k + n (1 <= n <= 8) and fills lanes 0 .. n - 1 from the
// top lanes of `fill`. AVX2 shifts bytes only within each 128-bit half, so the
// low half is first placed under the high one, with `fill` under the low half.
#define LANE_SHIFT(v, fill, n)                                                                     \
	_mm256_alignr_epi8((v), _mm256_permute2x128_si256((v), (fill), 0x02), 16 - 2 * (n))

static __m256i load(const int16_t *p) {
	return _mm256_loadu_si256((const __m256i *)p);
}

static void store(int16_t *p, __m256i v) {
	_mm256_storeu_si256((__m256i *)p, v);
}

Answer solve(const Input *in) {
	const char *s = in->s;
	const char *t = in->t;
	const size_t n = strlen(s);
	const size_t m = strlen(t);
	const size_t seg = (n + LANES - 1) / LANES;
	const size_t width = seg * LANES;

	// Row r of the grid (residue s[r]) lives in lane r / seg of vector r % seg,
	// so vector k holds rows k, seg + k, 2·seg + k, …, and the row above any row
	// is the same lane of vector k - 1. The profile holds, for each amino acid
	// a, the substitution score of a against every row in that layout. Rows
	// past n pad the last lane; no row above them reads them.
	int16_t *prof = (int16_t *)xmalloc(20 * width * sizeof *prof);
	for (size_t r = 0; r < width; r++) {
		const size_t at = (r % seg) * LANES + r / seg;
		const int code = r < n ? aa_index(s[r]) : 0;
		for (int a = 0; a < 20; a++) {
			prof[(size_t)a * width + at] = r < n ? (int16_t)BLOSUM62[code][a] : 0;
		}
	}

	// One column of the grid at a time. h holds max(M, X, Y) of the column
	// just finished and y its Y. Column 0 is a leading gap in t: X = -(11 + r)
	// at row r, and M = Y = -infinity.
	int16_t *h = (int16_t *)xmalloc(width * sizeof *h);
	int16_t *y = (int16_t *)xmalloc(width * sizeof *y);
	for (size_t r = 0; r < width; r++) {
		const size_t at = (r % seg) * LANES + r / seg;
		h[at] = (int16_t)(-GAP_OPEN - GAP_EXTEND * (long)r);
		y[at] = NEG;
	}

	// An X candidate loses GAP_EXTEND per row, so seg · GAP_EXTEND across a
	// whole lane. climb holds that loss times (lane + 1), drop times lane.
	int16_t steps[LANES];
	for (int lane = 0; lane < LANES; lane++) {
		steps[lane] = (int16_t)(GAP_EXTEND * (long)seg * (lane + 1));
	}
	const __m256i climb = load(steps);
	const __m256i drop =
	    _mm256_sub_epi16(climb, _mm256_set1_epi16((int16_t)(GAP_EXTEND * seg)));

	const __m256i open = _mm256_set1_epi16(GAP_OPEN);
	const __m256i extend = _mm256_set1_epi16(GAP_EXTEND);
	const __m256i neg = _mm256_set1_epi16(NEG);
	for (size_t j = 0; j < m; j++) {
		const int16_t *p = prof + (size_t)aa_index(t[j]) * width;

		// Each row's up-left cell is the row above in the column before: the
		// same lane one vector back or, for vector 0, the last vector in the
		// lane before. Row 0's is the gap row above the grid, 0 before column
		// 1 and -(11 + j - 1) before column j + 1.
		const int16_t corner =
		    j == 0 ? 0 : (int16_t)(-GAP_OPEN - GAP_EXTEND * (long)(j - 1));
		__m256i diag =
		    LANE_SHIFT(load(h + (seg - 1) * LANES), _mm256_set1_epi16(corner), 1);

		// A gap opens after any column: Y from the whole cell to the left, and
		// X from the M or Y of the cell above. X runs down the column, so each
		// vector hands the next one its X candidate for the row below. This
		// pass sees only candidates from rows of the same lane; the top row of
		// lane 0 opens from the gap row above the grid, the top row of every
		// other lane starts at -infinity, and the earlier lanes are settled
		// after the pass.
		const int16_t top = (int16_t)(-2 * GAP_OPEN - GAP_EXTEND * (long)j);
		__m256i down = _mm256_insert_epi16(neg, top, 0);
		for (size_t k = 0; k < seg; k++) {
			const size_t at = k * LANES;
			const __m256i h_left = load(h + at);
			const __m256i mv = _mm256_adds_epi16(diag, load(p + at));
			const __m256i yv = _mm256_max_epi16(
			    _mm256_subs_epi16(h_left, open), _mm256_subs_epi16(load(y + at), extend));
			store(h + at, _mm256_max_epi16(mv, _mm256_max_epi16(down, yv)));
			store(y + at, yv);
			down = _mm256_max_epi16(_mm256_subs_epi16(_mm256_max_epi16(mv, yv), open),
						_mm256_subs_epi16(down, extend));
			diag = h_left;
		}

		// down[L] is what lane L alone hands the top of lane L + 1. The top of
		// lane L gets the best of every earlier lane, each less one extension
		// per row in between: max over L' < L of down[L'] - e·seg·(L - 1 - L').
		// Adding e·seg·(L + 1) to down makes that a plain maximum over the
		// earlier lanes, a shift and four shift-and-max steps, and subtracting
		// e·seg·L gives the entry itself. One more pass hands each entry down
		// its lane, one extension per row.
		__m256i scan = LANE_SHIFT(_mm256_adds_epi16(down, climb), neg, 1);
		scan = _mm256_max_epi16(scan, LANE_SHIFT(scan, neg, 1));
		scan = _mm256_max_epi16(scan, LANE_SHIFT(scan, neg, 2));
		scan = _mm256_max_epi16(scan, LANE_SHIFT(scan, neg, 4));
		scan = _mm256_max_epi16(scan, LANE_SHIFT(scan, neg, 8));
		__m256i carry = _mm256_subs_epi16(scan, drop);
		for (size_t k = 0; k < seg; k++) {
			const size_t at = k * LANES;
			store(h + at, _mm256_max_epi16(load(h + at), carry));
			carry = _mm256_subs_epi16(carry, extend);
		}
	}

	const size_t last = n - 1;
	const Answer a = h[(last % seg) * LANES + last / seg];
	free(prof);
	free(h);
	free(y);
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	fprintf(out, "%lld\n", *a);
}

void answer_free(Answer *a) {
	(void)a;
}
