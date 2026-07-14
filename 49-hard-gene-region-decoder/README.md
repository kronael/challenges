# 49 — Hard — Gene Region Decoder

Given a DNA sequence and a scored state model, return the most likely state at
every base. A state can represent a biological region such as coding DNA,
non-coding DNA, or a frame-specific segment.

The model contains:

- a starting score for each state;
- a score for moving from one state to another between adjacent bases;
- a score for observing `A`, `C`, `G`, or `T` while in each state.

The score of a path is its starting score, plus every transition score, plus the
emission score at every base. The input guarantees one path has a strictly
higher score than every other path.

## Input

```json
{
  "sequence": "AACCG",
  "start": [0, -4],
  "transition": [[0, -2], [-2, 0]],
  "emission": [[3, -3, -3, -3], [-3, 3, 3, -3]]
}
```

Rows and columns use state indices starting at zero. Emission columns are
ordered `A`, `C`, `G`, `T`.

Constraints: `1 ≤ |sequence| ≤ 200,000`; `1 ≤ states ≤ 32`; all matrices have
matching dimensions; every score is a signed 32-bit integer; the best total
score fits in a signed 64-bit integer; `|sequence| · states² ≤ 20,000,000`.

## Output

Print the state index for every base, separated by spaces.

## Example

```text
{"sequence":"AACCG","start":[0,-4],"transition":[[0,-2],[-2,0]],"emission":[[3,-3,-3,-3],[-3,3,3,-3]]}
→ 0 0 1 1 1
```

## Run

```text
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.
