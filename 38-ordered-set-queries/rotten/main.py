import json
import sys


def solve(ops):
    # Naive sorted list with O(n) scans per op: correct, but TIMEOUTs on the large
    # cases — the trap. Every insert/delete/search/range_count walks the whole list.
    data = []
    out = []
    for op in ops:
        kind = op[0]
        if kind == "insert":
            v = op[1]
            i = 0
            while i < len(data) and data[i] < v:
                i += 1
            if i == len(data) or data[i] != v:
                data.insert(i, v)
        elif kind == "delete":
            v = op[1]
            i = 0
            while i < len(data) and data[i] < v:
                i += 1
            if i < len(data) and data[i] == v:
                data.pop(i)
        elif kind == "search":
            v = op[1]
            found = 0
            for x in data:
                if x == v:
                    found = 1
                    break
                if x > v:
                    break
            out.append(found)
        elif kind == "range_count":
            lo, hi = op[1], op[2]
            count = 0
            for x in data:
                if lo <= x <= hi:
                    count += 1
            out.append(count)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["ops"]))


if __name__ == "__main__":
    main()
