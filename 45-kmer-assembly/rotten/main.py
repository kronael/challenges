import json
import sys


def solve(k, kmers):
    # Naive O(n^2 * k): find the start read, then for each read scan all others
    # for the one whose (k-1) prefix matches this read's (k-1) suffix. Correct,
    # but it TIMEOUTs on the large cases — the trap.
    if not kmers:
        return ""
    p = k - 1
    n = len(kmers)
    used = [False] * n

    prefixes = [km[:p] for km in kmers]
    suffixes = [km[1:] for km in kmers]

    # Start read: the one whose (k-1) prefix is not any other read's suffix —
    # it has no predecessor. Found by scanning all pairs (O(n^2), the trap).
    start = 0
    for i in range(n):
        has_pred = False
        for j in range(n):
            if j != i and suffixes[j] == prefixes[i]:
                has_pred = True
                break
        if not has_pred:
            start = i
            break

    order = [start]
    used[start] = True
    cur = start
    for _ in range(n - 1):
        want = suffixes[cur]
        nxt = -1
        for j in range(n):
            if not used[j] and prefixes[j] == want:
                nxt = j
                break
        if nxt == -1:
            break
        used[nxt] = True
        order.append(nxt)
        cur = nxt

    out = [kmers[order[0]]]
    for idx in order[1:]:
        out.append(kmers[idx][-1])
    return "".join(out)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["kmers"]))


if __name__ == "__main__":
    main()
