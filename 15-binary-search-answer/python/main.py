import json
import sys


def solve(k, pages):
    # TODO: return the minimum possible value of the largest contiguous block sum
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["pages"]))


if __name__ == "__main__":
    main()
