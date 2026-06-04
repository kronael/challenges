import json
import sys


def solve(base, exp, mod):
    # TODO: return (base ** exp) % mod, computed in O(log exp)
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["base"], obj["exp"], obj["mod"]))


if __name__ == "__main__":
    main()
