import json
import sys


def solve(feeds):
    # Naive linear-scan merge: at every step, scan ALL feed heads to find the
    # smallest. Correct, but O(N*K) — it TIMEOUTs on the large cases (the trap).
    pos = [0] * len(feeds)
    out = []
    total = sum(len(f) for f in feeds)
    done = 0
    while done < total:
        best = None
        best_fi = -1
        for fi, feed in enumerate(feeds):
            j = pos[fi]
            if j >= len(feed):
                continue
            e = feed[j]
            key = (e["ts"], fi, e["id"])
            if best is None or key < best:
                best = key
                best_fi = fi
        e = feeds[best_fi][pos[best_fi]]
        out.append(e["ts"])
        out.append(e["id"])
        pos[best_fi] += 1
        done += 1
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["feeds"]))


if __name__ == "__main__":
    main()
