import json
import sys


def solve(horizontal, vertical):
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["horizontal"], obj["vertical"]))


if __name__ == "__main__":
    main()
