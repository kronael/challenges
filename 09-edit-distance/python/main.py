import json
import sys


def solve(s, t):
    # TODO: return the minimum number of single-character edits from s to t
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"], obj["t"]))


if __name__ == "__main__":
    main()
