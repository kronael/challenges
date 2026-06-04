import json
import sys


def solve(capacity, ops):
    # Naive: keep a flat HISTORY of every key touch, and to find the eviction
    # victim, scan the whole history for each cached key to locate its most recent
    # touch, taking the key whose latest touch is oldest. O(history) per eviction
    # makes the whole run O(n^2) — correct, but TIMEOUTs on the large cases — the trap.
    store = {}  # key -> value
    history = []  # every touched key, in order; history[-1] is the most recent
    out = []
    for op in ops:
        if op[0] == "get":
            key = op[1]
            if key in store:
                history.append(key)
                out.append(store[key])
            else:
                out.append(-1)
        else:  # put
            key, val = op[1], op[2]
            if key in store:
                store[key] = val
                history.append(key)
            else:
                store[key] = val
                history.append(key)
                if len(store) > capacity:
                    last_seen = {}
                    for i, k in enumerate(history):
                        if k in store:
                            last_seen[k] = i
                    lru_key = min(last_seen, key=lambda k: last_seen[k])
                    del store[lru_key]
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["capacity"], obj["ops"]))


if __name__ == "__main__":
    main()
