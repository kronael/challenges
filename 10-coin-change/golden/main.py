import json
import sys


def solve(amount, coins):
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["amount"], obj["coins"]))


if __name__ == "__main__":
    main()
