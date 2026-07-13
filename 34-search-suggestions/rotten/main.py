import json
import sys


def solve(words, queries):
    # Naive O(queries * |words|): re-scan the whole dictionary for every query,
    # collect prefix matches, sort, keep three. Correct, but TIMEOUTs at scale.
    results = []
    for q in queries:
        matches = []
        for w in words:
            if len(w) < len(q):
                continue
            ok = True
            for i in range(len(q)):
                if w[i] != q[i]:
                    ok = False
                    break
            if ok:
                matches.append(w)
        matches.sort()
        results.append(" ".join(matches[:3]))
    return ";".join(results)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["words"], obj["queries"]))


if __name__ == "__main__":
    main()
