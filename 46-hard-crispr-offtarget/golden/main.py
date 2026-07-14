import json
import sys


def solve(d, length, genome, guides):
    n = len(genome)
    if n < length or length == 0:
        return [0] * len(guides)

    starts = range(n - length + 1)

    # Pigeonhole: split length L into d+1 contiguous seeds. Any window within
    # Hamming distance d of a guide must match the guide exactly on at least one
    # seed. Index every genome window by (slot, seed) so a guide can fetch its
    # candidate windows instead of scanning all of them.
    bounds = [length * i // (d + 1) for i in range(d + 2)]
    index = [{} for _ in range(d + 1)]
    for s in starts:
        for k in range(d + 1):
            seed = genome[s + bounds[k] : s + bounds[k + 1]]
            index[k].setdefault(seed, []).append(s)

    out = []
    for g in guides:
        seen = set()
        count = 0
        for k in range(d + 1):
            seed = g[bounds[k] : bounds[k + 1]]
            for s in index[k].get(seed, ()):
                if s in seen:
                    continue
                seen.add(s)
                mism = 0
                for i in range(length):
                    if genome[s + i] != g[i]:
                        mism += 1
                        if mism > d:
                            break
                if mism <= d:
                    count += 1
        out.append(count)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["d"], obj["len"], obj["genome"], obj["guides"]))


if __name__ == "__main__":
    main()
