import json
import sys


def colored_edges(genome):
    partner = {}
    for chromosome in genome:
        nodes = []
        for block in chromosome:
            value = abs(block)
            if block > 0:
                nodes.extend((2 * value - 1, 2 * value))
            else:
                nodes.extend((2 * value, 2 * value - 1))
        size = len(nodes)
        for i in range(1, size, 2):
            a = nodes[i]
            b = nodes[(i + 1) % size]
            partner[a] = b
            partner[b] = a
    return partner


def solve(a, b):
    red = colored_edges(a)
    blue = colored_edges(b)
    seen = set()
    cycles = 0
    for start in red:
        if start in seen:
            continue
        cycles += 1
        node = start
        while node not in seen:
            seen.add(node)
            node = red[node]
            seen.add(node)
            node = blue[node]
    return len(red) // 2 - cycles


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["a"], obj["b"]))


if __name__ == "__main__":
    main()
