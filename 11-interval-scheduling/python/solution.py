import json
import sys


def solve(intervals):
    count = 0
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["intervals"]))


if __name__ == "__main__":
    main()
