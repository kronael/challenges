import heapq
import json
import sys


def solve(feeds):
    out = []
    h = []
    for fi, feed in enumerate(feeds):
        if feed:
            e = feed[0]
            heapq.heappush(h, (e["ts"], fi, e["id"], 0))
    while h:
        ts, fi, eid, j = heapq.heappop(h)
        out.append(ts)
        out.append(eid)
        nj = j + 1
        if nj < len(feeds[fi]):
            e = feeds[fi][nj]
            heapq.heappush(h, (e["ts"], fi, e["id"], nj))
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["feeds"]))


if __name__ == "__main__":
    main()
