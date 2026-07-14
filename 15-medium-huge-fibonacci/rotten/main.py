import json
import sys

MOD = 1_000_000_007


def solve(n):
    # Naive O(n) iteration: correct, but TIMEOUTs on the large cases — the trap.
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % MOD
    return a


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"]))


if __name__ == "__main__":
    main()
