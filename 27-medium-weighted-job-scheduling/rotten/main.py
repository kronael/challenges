import json
import sys


def solve(jobs):
    # Naive O(n^2) DP: sort by end, then for each job scan all earlier jobs to
    # find the best compatible predecessor. Correct, but TIMEOUTs on the large
    # case — the trap.
    jobs = sorted(jobs, key=lambda j: j[1])
    n = len(jobs)
    if n == 0:
        return 0
    dp = [0] * n
    best = 0
    for i in range(n):
        s, _, w = jobs[i]
        take = w
        for j in range(i):
            if jobs[j][1] <= s and dp[j] + w > take:
                take = dp[j] + w
        dp[i] = take
        if take > best:
            best = take
    return best


def main():
    obj = json.load(sys.stdin)
    jobs = [(j["start"], j["end"], j["weight"]) for j in obj["jobs"]]
    print(solve(jobs))


if __name__ == "__main__":
    main()
