import json
import sys


def solve(k, arr):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["k"], obj["arr"]))


if __name__ == "__main__":
    main()
