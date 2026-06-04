import json
import sys


def solve(k, kmers):
    # TODO: reconstruct and return the original DNA string from the k-mers
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["kmers"]))


if __name__ == "__main__":
    main()
