import json
import sys


def solve(masses, spectrum):
    pass


def main():
    obj = json.load(sys.stdin)
    result = solve(obj["masses"], obj["spectrum"])
    print("NONE" if result is None else " ".join(map(str, result)))


if __name__ == "__main__":
    main()
