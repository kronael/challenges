import heapq
import json
import sys


def solve(processes, events):
    by_sequence = {}
    for index, event in enumerate(events):
        sequence = event["clock"][event["process"]]
        by_sequence[(event["process"], sequence)] = index

    outgoing = [[] for _ in events]
    indegree = [0] * len(events)
    for index, event in enumerate(events):
        process = event["process"]
        sequence = event["clock"][process]
        dependencies = []
        if sequence > 1:
            dependencies.append(by_sequence[(process, sequence - 1)])
        for other in range(processes):
            if other != process and event["clock"][other] > 0:
                dependencies.append(by_sequence[(other, event["clock"][other])])
        indegree[index] = len(dependencies)
        for dependency in dependencies:
            outgoing[dependency].append(index)

    ready = [
        (event["id"], index)
        for index, event in enumerate(events)
        if indegree[index] == 0
    ]
    heapq.heapify(ready)
    order = []
    while ready:
        event_id, index = heapq.heappop(ready)
        order.append(event_id)
        for dependent in outgoing[index]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, (events[dependent]["id"], dependent))
    return order


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["processes"], obj["events"]))


if __name__ == "__main__":
    main()
