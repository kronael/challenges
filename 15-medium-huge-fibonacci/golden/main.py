import json
import sys

MOD = 1_000_000_007


def solve(n):
    # fast-doubling Fibonacci: returns (F(k), F(k+1)) mod MOD
    def fib(k):
        if k == 0:
            return 0, 1
        a, b = fib(k >> 1)
        c = a * ((2 * b - a) % MOD) % MOD
        d = (a * a + b * b) % MOD
        if k & 1:
            return d, (c + d) % MOD
        return c, d

    return fib(n)[0]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"]))


if __name__ == "__main__":
    main()
