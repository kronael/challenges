import json
import sys


def solve(stream):
    # TODO: return median after each insertion as a list of formatted strings
    # Format: "5" (odd count) or "4.5" (even count, one decimal)
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["stream"]))


if __name__ == "__main__":
    main()
