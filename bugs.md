# bugs

Review queue. Log here, do not fix unless explicitly asked.

## Rust challenges 08-30: digit-leading package names break the build

Every io rust challenge has `name = "NN-slug"` in `Cargo.toml` (e.g.
`08-lis`, `21-kmp`, `22-segment-tree`). Cargo rejects this:

```
error: invalid character `2` in package name: `22-segment-tree`,
the name cannot start with a digit
```

So `cargo build`, `cargo test`, and `make bench` all fail in `*/rust/` for
08-30. The `[[bin]]` blocks also set the same invalid `name`.

The `template/` itself is fine (`name = "challenge"`).

Fix options (pick one, apply to all 08-30):
- Prefix the package name, e.g. `name = "ch22-segment-tree"`, and update the
  Makefile `BIN_NAME` grep / `[[bin]]` accordingly.
- Or set a valid `name` plus an explicit `[[bin]] name` that the Makefile
  targets.

Affected (digit-leading rust package name): 08, 09, 10, 11, 12, 13, 14, 15,
16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30.

## Cargo.toml package vs dir-name drift (28, 29, 30)

The rust package name does not match the directory for three challenges:
- `28-prime-pair-sets/rust` -> `name = "28-josephus"`
- `29-distinct-substrings/rust` -> `name = "29-convex-hull"`
- `30-max-flow/rust` -> `name = "30-network-flow"`

The go.mod modules drift the same way (e.g. `30-network-flow`). The Makefile
derives the binary name from these files, so bench still targets the right
file, but the names are stale leftovers from earlier problem choices.
