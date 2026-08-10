import json
import sys
from bisect import bisect_right


def _reduce(reads):
    # Same correctness prep as the reference: distinct reads, drop any contained
    # in a longer one. Not the trap — the greedy merge below is.
    uniq = list(dict.fromkeys(reads))
    uniq.sort(key=len)
    lens = [len(r) for r in uniq]
    kept = []
    for i, r in enumerate(uniq):
        start = bisect_right(lens, len(r))
        if not any(r in uniq[j] for j in range(start, len(uniq))):
            kept.append(r)
    return kept


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
    frags = _reduce(reads)
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
