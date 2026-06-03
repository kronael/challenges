import json
import sys


def solve(base, exp, mod):
    if mod == 1:
        return 0
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["base"], obj["exp"], obj["mod"]))


if __name__ == "__main__":
    main()
