import json
import sys


def solve(s):
    # Naive: count each substring at its first occurrence, found by searching the
    # whole text again — n² substrings, each an O(n) slice and search, so O(n³)
    # time. It TIMEOUTs on the large cases.
    n = len(s)
    return sum(
        1 for i in range(n) for j in range(i + 1, n + 1) if s.find(s[i:j]) == i
    )


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"]))


if __name__ == "__main__":
    main()
