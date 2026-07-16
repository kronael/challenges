# 56 — Hard — Orthogonal Segment Crossings

**Task**: Count every crossing between horizontal and vertical segments.

**Difficulty**: hard
**Time estimate**: ~75 min

## Problem

You are given horizontal and vertical closed line segments with integer
coordinates. A horizontal segment is `[x1, x2, y]`. A vertical segment is
`[x, y1, y2]`. Endpoints may touch and count as intersections.

Count all horizontal-vertical pairs that intersect. Collinear pairs are not
part of the count. Several segments may cross at the same point; each pair is
counted separately.

Constraints: up to `200000` segments of each orientation, coordinates between
`-10^9` and `10^9`, with `x1 <= x2` and `y1 <= y2`.

## Input

```json
{"horizontal":[[0,5,2],[2,5,4]],"vertical":[[2,1,4],[5,0,5]]}
```

## Output

Print the number of intersecting pairs as one signed 64-bit integer. The result
can exceed the 32-bit range.

## Example

```text
4
```

## Run

```bash
make -C python
make -C go
make -C rust
```

Stuck? See `HINTS.md`.
