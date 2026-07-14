import json
import sys


def solve(k, kmers):
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["kmers"]))


if __name__ == "__main__":
    main()
