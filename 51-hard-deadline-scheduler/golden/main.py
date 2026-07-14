import heapq
import json
import sys


def solve(commands):
    clock = 0
    sequence = 0
    active = {}
    queue = []
    fired = []

    for command in commands:
        operation = command[0]
        if operation == "schedule":
            timer_id = command[1]
            sequence += 1
            entry = (clock + command[2], sequence)
            active[timer_id] = entry
            heapq.heappush(queue, (*entry, timer_id))
        elif operation == "cancel":
            active.pop(command[1], None)
        else:
            clock += command[1]
            while queue and queue[0][0] <= clock:
                deadline, order, timer_id = heapq.heappop(queue)
                if active.get(timer_id) != (deadline, order):
                    continue
                del active[timer_id]
                fired.append(timer_id)
    return fired


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["commands"]))


if __name__ == "__main__":
    main()
