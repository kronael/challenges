import json
import sys


def solve(s, t):
    # TODO: return the length of the longest common subsequence of s and t
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"], obj["t"]))


if __name__ == "__main__":
    main()
