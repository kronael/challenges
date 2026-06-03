import json
import sys


def solve(k, pages):
    def students_needed(limit):
        count = 1
        cur = 0
        for p in pages:
            if cur + p > limit:
                count += 1
                cur = p
            else:
                cur += p
        return count

    lo, hi = max(pages), sum(pages)
    while lo < hi:
        mid = (lo + hi) // 2
        if students_needed(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["pages"]))


if __name__ == "__main__":
    main()
