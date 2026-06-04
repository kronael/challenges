import json
import sys


def solve(seq):
    # TODO: return the length of the longest strictly increasing subsequence
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["seq"]))


if __name__ == "__main__":
    main()
