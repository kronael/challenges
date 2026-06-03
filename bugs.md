# bugs

Review queue. Log here, do not fix unless explicitly asked.

- 37-fenwick-tree: `cases/09_large_mixed.out` and `10_large_queries.out` lack a
  trailing newline while the solution's `print` emits one; values are identical
  byte-for-byte. Cosmetic only (test rstrips). All other challenges' `.out`
  files end in a newline; fenwick's small `.out` files also omit it. Inconsistent
  newline convention across the repo.
