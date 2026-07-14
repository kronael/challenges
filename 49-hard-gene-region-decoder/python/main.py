import json
import sys


def solve(sequence, start, transition, emission):
    pass


def main():
    obj = json.load(sys.stdin)
    print(
        *solve(
            obj["sequence"],
            obj["start"],
            obj["transition"],
            obj["emission"],
        )
    )


if __name__ == "__main__":
    main()
