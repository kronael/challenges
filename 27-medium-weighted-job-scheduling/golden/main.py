import json, sys
from bisect import bisect_right


def solve(jobs):
    # sort by end time
    jobs = sorted(jobs, key=lambda j: j[1])
    n = len(jobs)
    ends = [j[1] for j in jobs]

    # dp[i] = max weight using jobs 0..i-1
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        s, e, w = jobs[i - 1]
        # latest job that ends <= start of job i
        k = bisect_right(ends, s, hi=i - 1)
        dp[i] = max(dp[i - 1], dp[k] + w)

    return dp[n]


def main():
    obj = json.load(sys.stdin)
    jobs = [(j["start"], j["end"], j["weight"]) for j in obj["jobs"]]
    print(solve(jobs))


if __name__ == "__main__":
    main()
