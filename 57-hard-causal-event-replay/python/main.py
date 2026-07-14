import json
import sys


def solve(processes, events):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["processes"], obj["events"]))


if __name__ == "__main__":
    main()
