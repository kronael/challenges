import json
import sys


def solve(orders):
    # TODO: run the order book and return
    #   [num_trades, p1, q1, p2, q2, ..., best_bid, bid_qty, best_ask, ask_qty]
    _ = orders
    return []


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["orders"]))


if __name__ == "__main__":
    main()
