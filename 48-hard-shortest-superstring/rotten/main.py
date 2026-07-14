import json
import sys


def _overlap(a, b):
    # longest suffix of a that is a prefix of b, by sliding-window compare
    m = min(len(a), len(b))
    for k in range(m, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0


def solve(reads):
    # Naive greedy merge: every round, recompute the max overlap over ALL remaining
    # pairs by sliding-window string compare, merge the best pair, repeat. Correct on
    # the small cases, but O(n^3 * L) — it TIMEOUTs on the many-reads large case.
    frags = [r for r in reads if r]
    if not frags:
        return ""
    while len(frags) > 1:
        best_k = -1
        bi = bj = 0
        for i in range(len(frags)):
            for j in range(len(frags)):
                if i == j:
                    continue
                k = _overlap(frags[i], frags[j])
                if k > best_k:
                    best_k = k
                    bi, bj = i, j
        merged = frags[bi] + frags[bj][best_k:]
        a, b = sorted((bi, bj), reverse=True)
        frags.pop(a)
        frags.pop(b)
        frags.append(merged)
    return frags[0]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["reads"]))


if __name__ == "__main__":
    main()
