import json
import sys


def solve(s):
    # Naive: dump every substring into a set — correct, but quadratic memory and
    # cubic time. It TIMEOUTs and blows up on the large cases — the trap.
    n = len(s)
    seen = set()
    for i in range(n):
        for j in range(i + 1, n + 1):
            seen.add(s[i:j])
    return len(seen)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"]))


if __name__ == "__main__":
    main()
