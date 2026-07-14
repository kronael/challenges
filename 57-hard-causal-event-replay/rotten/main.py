import json
import sys


def solve(processes, events):
    delivered = [0] * processes
    pending = list(events)
    order = []
    while pending:
        chosen = None
        # Naive: rescan every pending vector clock after each emitted event.
        # Correct, but O(events² * processes) work TIMEOUTs on large histories.
        for event in pending:
            process = event["process"]
            clock = event["clock"]
            ready = clock[process] == delivered[process] + 1
            ready = ready and all(
                other == process or clock[other] <= delivered[other]
                for other in range(processes)
            )
            if ready and (chosen is None or event["id"] < chosen["id"]):
                chosen = event
        pending.remove(chosen)
        delivered[chosen["process"]] += 1
        order.append(chosen["id"])
    return order


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["processes"], obj["events"]))


if __name__ == "__main__":
    main()
