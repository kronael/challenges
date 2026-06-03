import json
import sys


def solve(words, queries):
    # TODO: build a trie; for each query return up to 3 lex-smallest completions
    # Return query results joined by ";", completions within a result joined by " "
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["words"], [q for q in obj["queries"]]))


if __name__ == "__main__":
    main()
