import json
import sys


def solve(n, friendships, queries):
    # Naive relabeling: each person carries a component label; a union rescans all
    # n people and relabels one whole group into the other. Correct, but
    # O(friendships*n) — it TIMEOUTs on the large cases (the trap).
    comp = list(range(n))
    for a, b in friendships:
        ca, cb = comp[a], comp[b]
        if ca == cb:
            continue
        for i in range(n):
            if comp[i] == cb:
                comp[i] = ca
    return [1 if comp[u] == comp[v] else 0 for u, v in queries]


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["friendships"], obj["queries"]))


if __name__ == "__main__":
    main()
