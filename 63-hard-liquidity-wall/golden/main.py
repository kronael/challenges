import json
import sys


def solve(n, quantities):
    # One pass with a stack of level indices whose resting quantities increase
    # from the bottom up. A level stays on the stack while every level scanned
    # since it was pushed rests at least as much, so the moment a shallower level
    # arrives is the moment that level's widest run is settled: it reaches from
    # the level still below it on the stack, exclusive, to the shallower level,
    # exclusive. Index -1 and index n act as levels resting nothing, which is why
    # the loop runs to n and why an empty stack means the run starts at 0.
    # Every index is pushed once and popped once, so the whole book costs O(n).
    best = 0
    stack = []
    for right in range(n + 1):
        height = quantities[right] if right < n else 0
        while stack and quantities[stack[-1]] >= height:
            top = stack.pop()
            left = stack[-1] if stack else -1
            area = quantities[top] * (right - left - 1)
            if area > best:
                best = area
        stack.append(right)
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["quantities"]))


if __name__ == "__main__":
    main()
