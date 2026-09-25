import json
import sys


def solve(n, slippage, ks):
    del n
    out = []
    for k in ks:
        rest = list(slippage)
        # Naive O(n*k) repeated extraction: every one of the k-1 rounds rescans
        # the whole remaining log for its maximum and drops it, so a rank of k
        # costs k full passes over n fills. Correct, but the large cases ask for
        # ranks in the hundreds of thousands, so it TIMEOUTs.
        for _ in range(k - 1):
            rest.remove(max(rest))
        out.append(max(rest))
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["slippage"], obj["ks"]))


if __name__ == "__main__":
    main()
