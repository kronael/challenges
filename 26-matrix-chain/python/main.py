import json
import sys


def solve(dims):
    # TODO: return the minimum number of scalar multiplications
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["dims"]))


if __name__ == "__main__":
    main()
