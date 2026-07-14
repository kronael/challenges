# Hints — 51 Hard — Deadline Scheduler

> Spoilers. Open only when stuck.

- Keep active timers in a min-heap ordered by `(deadline, insertion_order)`.
  An `advance` then jumps directly to expired timers instead of visiting every
  clock tick.
- Cancellation and replacement are awkward because a basic heap cannot remove
  an arbitrary entry cheaply. Keep the current `(deadline, insertion_order)`
  for each ID in a hash map. Leave old heap entries in place and discard one
  when it reaches the top unless it still matches the map.
- Each schedule costs `O(log n)`, cancel costs expected `O(1)`, and every heap
  entry is pushed and popped once. Clock jumps do not affect the running time.
- The rotten reference advances one tick at a time and scans every active timer
  on every tick. A few timers and one large jump are enough to time it out.
- Production timer facilities make different choices based on clock precision,
  deadline range, cancellation rate, and latency requirements. The sources
  below are worth reading after the challenge.

Sources:

- Varghese and Lauck's timer-facility paper compares queueing structures and
  introduces hashed and hierarchical timing wheels:
  https://doi.org/10.1145/37499.37504
- Linux high-resolution timers use a time-ordered tree and explain why that
  design is separate from the low-resolution timer wheel:
  https://www.kernel.org/doc/html/latest/timers/hrtimers.html
