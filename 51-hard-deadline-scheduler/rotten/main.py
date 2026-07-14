import json
import sys


def solve(commands):
    # Naive: advance every clock tick and rescan every active timer on that tick.
    # Correct, but O(total_advanced_time * active_timers) TIMEOUTs on large jumps.
    clock = 0
    sequence = 0
    active = {}
    fired = []

    for command in commands:
        operation = command[0]
        if operation == "schedule":
            sequence += 1
            active[command[1]] = (clock + command[2], sequence)
        elif operation == "cancel":
            active.pop(command[1], None)
        else:
            ticks = command[1]
            checkpoints = [clock] if ticks == 0 else range(clock + 1, clock + ticks + 1)
            for current in checkpoints:
                clock = current
                due = sorted(
                    (
                        deadline,
                        order,
                        timer_id,
                    )
                    for timer_id, (deadline, order) in active.items()
                    if deadline <= clock
                )
                for _, _, timer_id in due:
                    del active[timer_id]
                    fired.append(timer_id)
    return fired


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["commands"]))


if __name__ == "__main__":
    main()
