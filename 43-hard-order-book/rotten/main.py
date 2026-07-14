import json
import sys


def solve(orders):
    # Naive engine: the book is one flat list of resting orders. For every
    # incoming order we re-sort and linearly scan the whole list to find the
    # best opposite level. Correct, but the per-order O(n) scan makes the whole
    # run O(n^2) — it TIMEOUTs on the large cases. That's the trap.
    bids = []  # list of [price, qty], time order preserved by append
    asks = []  # list of [price, qty]
    trades = []  # flat: price, qty, price, qty, ...

    for o in orders:
        side = o["side"]
        otype = o["type"]
        price = o["price"]
        qty = o["qty"]

        if side == "buy":
            while qty > 0:
                # Rescan the whole ask book for the best (lowest) live price,
                # earliest arrival as tiebreak.
                best_i = -1
                for i in range(len(asks)):
                    if asks[i][1] <= 0:
                        continue
                    if best_i == -1 or asks[i][0] < asks[best_i][0]:
                        best_i = i
                if best_i == -1:
                    break
                bp = asks[best_i][0]
                if otype == "limit" and bp > price:
                    break
                avail = asks[best_i][1]
                take = avail if avail <= qty else qty
                trades.append(bp)
                trades.append(take)
                qty -= take
                asks[best_i][1] -= take
            if otype == "limit" and qty > 0:
                bids.append([price, qty])
        else:
            while qty > 0:
                best_i = -1
                for i in range(len(bids)):
                    if bids[i][1] <= 0:
                        continue
                    if best_i == -1 or bids[i][0] > bids[best_i][0]:
                        best_i = i
                if best_i == -1:
                    break
                bp = bids[best_i][0]
                if otype == "limit" and bp < price:
                    break
                avail = bids[best_i][1]
                take = avail if avail <= qty else qty
                trades.append(bp)
                trades.append(take)
                qty -= take
                bids[best_i][1] -= take
            if otype == "limit" and qty > 0:
                asks.append([price, qty])

    bb, bb_qty = 0, 0
    for p, q in bids:
        if q > 0 and (bb == 0 or p > bb):
            bb = p
    if bb:
        bb_qty = sum(q for p, q in bids if p == bb and q > 0)

    ba, ba_qty = 0, 0
    for p, q in asks:
        if q > 0 and (ba == 0 or p < ba):
            ba = p
    if ba:
        ba_qty = sum(q for p, q in asks if p == ba and q > 0)

    out = [len(trades) // 2]
    out.extend(trades)
    out.extend([bb, bb_qty, ba, ba_qty])
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["orders"]))


if __name__ == "__main__":
    main()
