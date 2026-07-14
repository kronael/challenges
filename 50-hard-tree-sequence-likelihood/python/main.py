import json
import sys


def solve(parent, sequences, prior, transition):
    pass


def main():
    obj = json.load(sys.stdin)
    result = solve(
        obj["parent"],
        obj["sequences"],
        obj["prior"],
        obj["transition"],
    )
    print(f"{result:.6f}")


if __name__ == "__main__":
    main()
