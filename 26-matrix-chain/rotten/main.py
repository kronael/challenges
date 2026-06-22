import json
import sys


def solve(dims):
    n = len(dims) - 1
    if n <= 1:
        return 0

    def cost(i, j):
        if i == j:
            return 0
        best = float("inf")
        for k in range(i, j):
            c = cost(i, k) + cost(k + 1, j) + dims[i] * dims[k + 1] * dims[j + 1]
            if c < best:
                best = c
        return best

    return cost(0, n - 1)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["dims"]))


if __name__ == "__main__":
    main()
