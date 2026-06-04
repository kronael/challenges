import heapq
import json
import sys
from collections import deque


def solve(orders):
    # Price-time priority book. Per side a heap of price levels (bids as a
    # max-heap via negated price, asks as a min-heap) and, per price level, a
    # FIFO queue of resting quantities plus a running total. Lazy deletion drops
    # levels whose total has fallen to zero, so the best price is O(1) amortised.
    bid_heap = []  # -price
    ask_heap = []  # price
    bid_q = {}  # price -> deque of resting quantities (FIFO)
    ask_q = {}  # price -> deque of resting quantities (FIFO)
    bid_tot = {}  # price -> total resting quantity
    ask_tot = {}  # price -> total resting quantity
    trades = []  # flat list: price, qty, price, qty, ...

    def best_bid():
        while bid_heap:
            p = -bid_heap[0]
            if bid_tot.get(p, 0) > 0:
                return p
            heapq.heappop(bid_heap)
            bid_q.pop(p, None)
            bid_tot.pop(p, None)
        return 0

    def best_ask():
        while ask_heap:
            p = ask_heap[0]
            if ask_tot.get(p, 0) > 0:
                return p
            heapq.heappop(ask_heap)
            ask_q.pop(p, None)
            ask_tot.pop(p, None)
        return 0

    def rest(side, price, qty):
        if qty <= 0:
            return
        if side == "buy":
            if price not in bid_q:
                bid_q[price] = deque()
                bid_tot[price] = 0
                heapq.heappush(bid_heap, -price)
            bid_q[price].append(qty)
            bid_tot[price] += qty
        else:
            if price not in ask_q:
                ask_q[price] = deque()
                ask_tot[price] = 0
                heapq.heappush(ask_heap, price)
            ask_q[price].append(qty)
            ask_tot[price] += qty

    for o in orders:
        side = o["side"]
        otype = o["type"]
        price = o["price"]
        qty = o["qty"]

        if side == "buy":
            # Match against asks, lowest first.
            while qty > 0:
                bp = best_ask()
                if bp == 0:
                    break
                if otype == "limit" and bp > price:
                    break
                q = ask_q[bp]
                while qty > 0 and q:
                    avail = q[0]
                    take = avail if avail <= qty else qty
                    trades.append(bp)
                    trades.append(take)
                    qty -= take
                    ask_tot[bp] -= take
                    if take == avail:
                        q.popleft()
                    else:
                        q[0] = avail - take
            if otype == "limit":
                rest("buy", price, qty)
        else:
            # Match against bids, highest first.
            while qty > 0:
                bp = best_bid()
                if bp == 0:
                    break
                if otype == "limit" and bp < price:
                    break
                q = bid_q[bp]
                while qty > 0 and q:
                    avail = q[0]
                    take = avail if avail <= qty else qty
                    trades.append(bp)
                    trades.append(take)
                    qty -= take
                    bid_tot[bp] -= take
                    if take == avail:
                        q.popleft()
                    else:
                        q[0] = avail - take
            if otype == "limit":
                rest("sell", price, qty)

    bb = best_bid()
    ba = best_ask()
    out = [len(trades) // 2]
    out.extend(trades)
    out.extend([bb, bid_tot.get(bb, 0) if bb else 0, ba, ask_tot.get(ba, 0) if ba else 0])
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["orders"]))


if __name__ == "__main__":
    main()
