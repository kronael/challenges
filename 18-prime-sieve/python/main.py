import json
import sys


def solve(n):
    # TODO: return the number of primes p with p < n
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"]))


if __name__ == "__main__":
    main()
