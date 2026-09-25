import json
import sys


def solve(capacity, ops):
    # Naive: stamp each key with the tick of its last use, then find the eviction
    # victim by scanning every cached key for the smallest stamp. Correct, but that
    # scan is O(capacity) per eviction, so a full cache makes the run O(n·capacity)
    # — it TIMEOUTs on the large cases. That is the trap.
    store = {}  # key -> value
    last_used = {}  # key -> tick of its most recent get/put
    out = []
    for tick, op in enumerate(ops):
        if op[0] == "get":
            key = op[1]
            if key in store:
                last_used[key] = tick
                out.append(store[key])
            else:
                out.append(-1)
        else:  # put
            key, val = op[1], op[2]
            store[key] = val
            last_used[key] = tick
            if len(store) > capacity:
                victim = min(last_used, key=last_used.get)
                del store[victim]
                del last_used[victim]
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["capacity"], obj["ops"]))


if __name__ == "__main__":
    main()
