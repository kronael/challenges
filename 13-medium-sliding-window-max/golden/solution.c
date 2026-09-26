#include "solution.h"

#include <immintrin.h>
#include <stdlib.h>

void input_parse(const JsonValue *root, Input *in) {
	in->k = (int)json_int(json_get(root, "k"));
	const JsonValue *arr = json_get(root, "arr");
	in->arr_len = json_len(arr);
	in->arr = (int32_t *)xmalloc(in->arr_len * sizeof *in->arr);
	for (size_t i = 0; i < in->arr_len; i++) {
		in->arr[i] = (int32_t)json_int(json_at(arr, i));
	}
}

void input_free(Input *in) {
	free(in->arr);
	in->arr = NULL;
	in->arr_len = 0;
}

// Lane j holds (first + j) mod k: how far reading first + j sits into its block.
static __m256i block_offsets(size_t first, size_t k) {
	int32_t lane[8];
	for (size_t j = 0; j < 8; j++) {
		lane[j] = (int32_t)((first + j) % k);
	}
	return _mm256_loadu_si256((const __m256i *)lane);
}

// (x + 8 mod k) mod k in every lane, from x + step and x + step - k side by
// side: the sum is below 2k, and when it is below k the difference is negative,
// which is huge read unsigned, so the unsigned minimum is the reduced value.
static __m256i advance(__m256i x, __m256i step, __m256i back) {
	return _mm256_min_epu32(_mm256_add_epi32(x, step), _mm256_add_epi32(x, back));
}

// max(v, from) in the lanes `take` selects, v elsewhere.
static __m256i fold(__m256i v, __m256i from, __m256i take) {
	return _mm256_max_epi32(v, _mm256_blendv_epi8(v, from, take));
}

// Lane j becomes the maximum of lanes 0..j: two shifts inside each 128-bit
// half, then the low half's top lane raises the high half.
static __m256i rise(__m256i v) {
	const __m256i low = _mm256_set1_epi32(INT32_MIN);
	v = _mm256_max_epi32(v, _mm256_alignr_epi8(v, low, 12));
	v = _mm256_max_epi32(v, _mm256_alignr_epi8(v, low, 8));
	const __m256i third = _mm256_setr_epi32(0, 0, 0, 0, 3, 3, 3, 3);
	return _mm256_max_epi32(v, _mm256_permutevar8x32_epi32(v, third));
}

// Lane j becomes the maximum of lanes j..7, the mirror of rise.
static __m256i fall(__m256i v) {
	const __m256i low = _mm256_set1_epi32(INT32_MIN);
	v = _mm256_max_epi32(v, _mm256_alignr_epi8(low, v, 4));
	v = _mm256_max_epi32(v, _mm256_alignr_epi8(low, v, 8));
	const __m256i fourth = _mm256_setr_epi32(4, 4, 4, 4, 7, 7, 7, 7);
	return _mm256_max_epi32(v, _mm256_permutevar8x32_epi32(v, fourth));
}

// pre[i]: the maximum of arr from the start of i's block of k readings to i.
// `at` is the first lane's offset into its block. A step whose eight readings
// share one block takes the running maximum across all lanes, then the carry
// from the step before unless this step opens the block. A step that a block
// start splits builds the same thing in masked shifts: each shift of 1, 2, and
// 4 lanes is kept only in the lanes it does not carry across a block start,
// and the carry joins only the lanes whose block began before this step.
static void scan_forward(const int32_t *a, size_t n, size_t k, int32_t *pre) {
	const size_t step = 8 % k;
	const __m256i steps = _mm256_set1_epi32((int32_t)step);
	const __m256i back = _mm256_set1_epi32((int32_t)step - (int32_t)k);
	const __m256i low = _mm256_set1_epi32(INT32_MIN);
	const __m256i lanes = _mm256_setr_epi32(0, 1, 2, 3, 4, 5, 6, 7);
	const __m256i back1 = _mm256_setr_epi32(0, 0, 1, 2, 3, 4, 5, 6);
	const __m256i back2 = _mm256_setr_epi32(0, 0, 0, 1, 2, 3, 4, 5);
	const __m256i back4 = _mm256_setr_epi32(0, 0, 0, 0, 0, 1, 2, 3);
	const __m256i top = _mm256_set1_epi32(7);
	__m256i off = block_offsets(0, k);
	__m256i carry = low;
	size_t at = 0;
	size_t i = 0;
	for (; i + 8 <= n; i += 8) {
		__m256i v = _mm256_loadu_si256((const __m256i *)(a + i));
		if (at + 8 <= k) {
			if (at == 0) {
				carry = low;
			}
			v = rise(v);
			_mm256_storeu_si256((__m256i *)(pre + i), _mm256_max_epi32(v, carry));
			carry = _mm256_max_epi32(carry, _mm256_permutevar8x32_epi32(v, top));
		} else {
			v = fold(v, _mm256_permutevar8x32_epi32(v, back1),
				 _mm256_cmpgt_epi32(off, _mm256_set1_epi32(0)));
			v = fold(v, _mm256_permutevar8x32_epi32(v, back2),
				 _mm256_cmpgt_epi32(off, _mm256_set1_epi32(1)));
			v = fold(v, _mm256_permutevar8x32_epi32(v, back4),
				 _mm256_cmpgt_epi32(off, _mm256_set1_epi32(3)));
			v = fold(v, carry, _mm256_cmpgt_epi32(off, lanes));
			_mm256_storeu_si256((__m256i *)(pre + i), v);
			carry = _mm256_permutevar8x32_epi32(v, top);
		}
		off = advance(off, steps, back);
		at = at + step < k ? at + step : at + step - k;
	}
	for (; i < n; i++) {
		pre[i] = i % k == 0 || a[i] > pre[i - 1] ? a[i] : pre[i - 1];
	}
}

// suf[i]: the maximum of arr from i to the end of i's block, or to the last
// reading when that comes first. The mirror of scan_forward, walking down from
// the top: `rem` counts the readings after each lane's reading in its block.
static void scan_backward(const int32_t *a, size_t n, size_t k, int32_t *suf) {
	const size_t step = 8 % k;
	const __m256i steps = _mm256_set1_epi32((int32_t)step);
	const __m256i back = _mm256_set1_epi32((int32_t)step - (int32_t)k);
	const __m256i last = _mm256_set1_epi32((int32_t)k - 1);
	const __m256i low = _mm256_set1_epi32(INT32_MIN);
	const __m256i ahead = _mm256_setr_epi32(7, 6, 5, 4, 3, 2, 1, 0);
	const __m256i next1 = _mm256_setr_epi32(1, 2, 3, 4, 5, 6, 7, 7);
	const __m256i next2 = _mm256_setr_epi32(2, 3, 4, 5, 6, 7, 7, 7);
	const __m256i next4 = _mm256_setr_epi32(4, 5, 6, 7, 7, 7, 7, 7);
	const __m256i bottom = _mm256_setzero_si256();
	size_t i = n & ~(size_t)7;
	for (size_t j = n; j-- > i;) {
		const int ends = j + 1 == n || (j + 1) % k == 0;
		suf[j] = ends || a[j] > suf[j + 1] ? a[j] : suf[j + 1];
	}
	if (i == 0) {
		return;
	}
	size_t at = (i - 8) % k;
	__m256i rem = _mm256_sub_epi32(last, block_offsets(i - 8, k));
	__m256i carry = _mm256_set1_epi32(i < n ? suf[i] : INT32_MIN);
	while (i > 0) {
		i -= 8;
		__m256i v = _mm256_loadu_si256((const __m256i *)(a + i));
		if (at + 8 <= k) {
			if (at + 8 == k) {
				carry = low;
			}
			v = fall(v);
			_mm256_storeu_si256((__m256i *)(suf + i), _mm256_max_epi32(v, carry));
			carry = _mm256_max_epi32(carry, _mm256_permutevar8x32_epi32(v, bottom));
		} else {
			v = fold(v, _mm256_permutevar8x32_epi32(v, next1),
				 _mm256_cmpgt_epi32(rem, _mm256_set1_epi32(0)));
			v = fold(v, _mm256_permutevar8x32_epi32(v, next2),
				 _mm256_cmpgt_epi32(rem, _mm256_set1_epi32(1)));
			v = fold(v, _mm256_permutevar8x32_epi32(v, next4),
				 _mm256_cmpgt_epi32(rem, _mm256_set1_epi32(3)));
			v = fold(v, carry, _mm256_cmpgt_epi32(rem, ahead));
			_mm256_storeu_si256((__m256i *)(suf + i), v);
			carry = _mm256_permutevar8x32_epi32(v, bottom);
		}
		rem = advance(rem, steps, back);
		at = at >= step ? at - step : at + k - step;
	}
}

Answer solve(const Input *in) {
	const size_t n = in->arr_len;
	const size_t k = (size_t)in->k;
	const size_t m = n - k + 1;
	int32_t *pre = (int32_t *)xmalloc(n * sizeof *pre);
	int32_t *suf = (int32_t *)xmalloc(n * sizeof *suf);
	int32_t *peak = (int32_t *)xmalloc(m * sizeof *peak);

	// Blocks of k readings start at every multiple of k, so the window
	// i..i+k-1 is the tail of one block and the head of the next: its maximum
	// is suf[i] against pre[i+k-1], and this loop vectorizes as written.
	scan_forward(in->arr, n, k, pre);
	scan_backward(in->arr, n, k, suf);
	for (size_t i = 0; i < m; i++) {
		const int32_t tail = suf[i];
		const int32_t head = pre[i + k - 1];
		peak[i] = tail > head ? tail : head;
	}

	free(pre);
	free(suf);
	Answer a = {peak, m};
	return a;
}

void answer_print(FILE *out, const Answer *a) {
	for (size_t i = 0; i < a->n; i++) {
		if (i > 0) {
			fputc(' ', out);
		}
		fprintf(out, "%d", a->v[i]);
	}
	fputc('\n', out);
}

void answer_free(Answer *a) {
	free(a->v);
	a->v = NULL;
	a->n = 0;
}
