import json
import sys


def solve(text, pattern):
    # Naive O(|T|*|P|) scan: try the pattern at every start position, comparing
    # character by character. Correct, but TIMEOUTs on the large cases — the trap.
    m = len(pattern)
    if m == 0:
        return []
    n = len(text)
    res = []
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            res.append(i + 1)
    return res


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["text"], obj["pattern"]))


if __name__ == "__main__":
    main()
