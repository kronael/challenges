import json
import sys


def solve(n, operations):
    active = set()
    answers = []
    for op in operations:
        edge = tuple(sorted((op["u"], op["v"])))
        if op["type"] == "add":
            active.add(edge)
        elif op["type"] == "remove":
            active.remove(edge)
        else:
            # Naive: rebuild the whole live graph and search it for every ask.
            # Correct, but O(q(n+m)) repeated work TIMEOUTs on large histories.
            graph = [[] for _ in range(n)]
            for a, b in active:
                graph[a].append(b)
                graph[b].append(a)
            seen = {op["u"]}
            stack = [op["u"]]
            while stack:
                node = stack.pop()
                for neighbor in graph[node]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            answers.append(int(op["v"] in seen))
    return answers


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["operations"]))


if __name__ == "__main__":
    main()
