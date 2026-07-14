import json
import sys


def solve(amount, coins):
    # Naive O(amount^2) DP: instead of scanning the (few) coins per amount, it splits
    # every amount `a` into all pairs (j, a-j) and asks whether `a-j` is a coin. Correct,
    # but quadratic in `amount` — it TIMEOUTs on the large cases. The trap.
    coinset = set(coins)
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for j in range(a):
            if (a - j) in coinset and dp[j] + 1 < dp[a]:
                dp[a] = dp[j] + 1
    return -1 if dp[amount] == INF else dp[amount]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["amount"], obj["coins"]))


if __name__ == "__main__":
    main()
