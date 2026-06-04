import json
import sys

GAP_OPEN = 11
GAP_EXTEND = 1

AA = "ARNDCQEGHILKMFPSTWYV"

# BLOSUM62 substitution scores, rows/cols in AA order.
BLOSUM62 = [
    [4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, -3, -2, 0],
    [-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -2, -3],
    [-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -4, -2, -3],
    [-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -4, -3, -3],
    [0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1],
    [-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2],
    [-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -3, -2, -2],
    [0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3],
    [-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, 2, -3],
    [-1, -3, -3, -3, -1, -3, -3, -4, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, 3],
    [-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -1, -2, -1, 1],
    [-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -1, -3, -1, 0, -1, -3, -2, -2],
    [-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -1, 5, 0, -2, -1, -1, -1, -1, 1],
    [-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 0, 6, -4, -2, -2, 1, 3, -1],
    [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2],
    [1, -1, 1, 0, -1, 0, 0, 0, -1, -2, -2, 0, -1, -2, -1, 4, 1, -3, -2, -2],
    [0, -1, 0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1, 5, -2, -2, 0],
    [-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1, -4, -3, -2, 11, 2, -3],
    [-2, -2, -2, -3, -2, -1, -2, -3, 2, -1, -1, -2, -1, 3, -3, -2, -2, 2, 7, -1],
    [0, -3, -3, -3, -1, -2, -2, -3, -3, 3, 1, -2, 1, -1, -2, -2, 0, -3, -1, 4],
]

IDX = {c: i for i, c in enumerate(AA)}


def solve(s, t):
    n, m = len(s), len(t)
    sub = BLOSUM62
    si = [IDX[c] for c in s]
    ti = [IDX[c] for c in t]
    NEG = float("-inf")
    # M: ends in match/mismatch; X: ends in gap in t (consume s); Y: gap in s (consume t).
    prev_m = [0] + [NEG] * m
    prev_x = [NEG] * (m + 1)
    prev_y = [NEG] * (m + 1)
    # First row: align prefix of t against gaps.
    for j in range(1, m + 1):
        prev_y[j] = -GAP_OPEN - GAP_EXTEND * (j - 1)
    for i in range(1, n + 1):
        cur_m = [NEG] * (m + 1)
        cur_x = [NEG] * (m + 1)
        cur_y = [NEG] * (m + 1)
        cur_x[0] = -GAP_OPEN - GAP_EXTEND * (i - 1)
        row = sub[si[i - 1]]
        for j in range(1, m + 1):
            best_prev = prev_m[j - 1]
            if prev_x[j - 1] > best_prev:
                best_prev = prev_x[j - 1]
            if prev_y[j - 1] > best_prev:
                best_prev = prev_y[j - 1]
            cur_m[j] = best_prev + row[ti[j - 1]]
            open_x = prev_m[j] - GAP_OPEN
            ext_x = prev_x[j] - GAP_EXTEND
            cur_x[j] = open_x if open_x > ext_x else ext_x
            open_y = cur_m[j - 1] - GAP_OPEN
            ext_y = cur_y[j - 1] - GAP_EXTEND
            cur_y[j] = open_y if open_y > ext_y else ext_y
        prev_m, prev_x, prev_y = cur_m, cur_x, cur_y
    return int(max(prev_m[m], prev_x[m], prev_y[m]))


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"], obj["t"]))


if __name__ == "__main__":
    main()
