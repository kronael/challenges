import json
import sys


def solve(reads):
    n = len(reads)
    if n == 0:
        return ""
    if n == 1:
        return reads[0]

    # Each read's true successor overlaps it by MORE THAN HALF the read's length.
    # For an overlap of length k (k > len(a) // 2) the suffix a[-k:] equals the
    # prefix b[:k]. Index every read by each prefix longer than half its length,
    # then probe each read's long suffixes (longest first) to find its unique
    # successor in O(L). Walk the chain once for an O(n * L) assembly.

    by_len = {}
    for i, r in enumerate(reads):
        m = len(r)
        for k in range(m // 2 + 1, m):
            by_len.setdefault(k, {}).setdefault(r[:k], []).append(i)

    succ = [-1] * n
    overlap = [0] * n
    has_pred = [False] * n
    for i, r in enumerate(reads):
        m = len(r)
        for k in range(m - 1, m // 2, -1):
            bucket = by_len.get(k)
            if not bucket:
                continue
            cands = bucket.get(r[-k:])
            if not cands:
                continue
            j = next((c for c in cands if c != i), -1)
            if j != -1:
                succ[i] = j
                overlap[i] = k
                has_pred[j] = True
                break

    start = next(i for i in range(n) if not has_pred[i])

    out = [reads[start]]
    cur = start
    seen = 1
    while succ[cur] != -1 and seen < n:
        nxt = succ[cur]
        out.append(reads[nxt][overlap[cur] :])
        cur = nxt
        seen += 1
    return "".join(out)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["reads"]))


if __name__ == "__main__":
    main()
