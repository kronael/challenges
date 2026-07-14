import json
import sys


def solve(rna, min_loop, allow_wobble):
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["rna"], obj["min_loop"], obj["allow_wobble"]))


if __name__ == "__main__":
    main()
