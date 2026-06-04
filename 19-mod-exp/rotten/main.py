import json
import sys


def solve(base, exp, mod):
    # Naive O(exp) loop: multiply by base one step at a time. Correct, but it
    # TIMEOUTs on the large cases (exp up to 10^18) — the trap.
    if mod == 1:
        return 0
    result = 1
    base %= mod
    for _ in range(exp):
        result = result * base % mod
    return result


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["base"], obj["exp"], obj["mod"]))


if __name__ == "__main__":
    main()
