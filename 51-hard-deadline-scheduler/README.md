# 51 — Hard — Deadline Scheduler

Process timer commands against a monotonic integer clock. The clock starts at
zero.

- `["schedule", id, delay]` schedules `id` at `clock + delay`. Scheduling an
  active ID replaces its old deadline and gives it a new insertion order.
- `["cancel", id]` removes an active timer. Cancelling any other ID does
  nothing.
- `["advance", delta]` moves the clock forward by `delta`, then fires every
  active timer whose deadline is no later than the new clock value.

Timers fired by one or more `advance` commands are printed in deadline order.
Timers sharing a deadline use their schedule insertion order. Firing removes a
timer. An advance of zero still fires timers due at the current clock value.

## Input

```json
{
  "commands": [
    ["schedule", 10, 5],
    ["schedule", 20, 2],
    ["advance", 5]
  ]
}
```

Constraints: at most `500,000` commands; IDs are signed 32-bit integers; delay,
delta, and the final clock value are integers from `0` through `10¹²`.

## Output

Print fired timer IDs separated by spaces. Print an empty line if no timer
fires.

## Examples

**Example 1** — scheduled second but due sooner, so it fires first
```text
{"commands":[["schedule",10,5],["schedule",20,2],["advance",5]]}
→ 20 10
```

**Example 2** — a cancelled timer never fires, a tied deadline fires in
schedule order, and an advance of zero still fires a timer due exactly now
```text
{"commands":[["schedule",1,5],["schedule",2,5],["schedule",3,2],["cancel",3],["advance",5],["schedule",4,0],["advance",0]]}
→ 1 2 4
```

## Run

```text
make -C rust
make -C go
make -C c
make -C python
```

Stuck? See `hints/01.md`.
