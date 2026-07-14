# 25 — Medium — Running Median

**Task**: Read a stream of integers and report the median after each insertion.

**Difficulty**: medium
**Time estimate**: ~45 min

## Problem

You are given a stream of `n` integers, arriving one at a time. After every
number arrives, output the median of all values seen so far: the middle value
when the count is odd, the average of the two middle values when the count is
even.

Constraints: `n` up to 2·10⁵, values fit in i32.

## Input

```json
{"stream": [1, 2, 3, 4]}
```

## Output

Space-separated medians, one per insertion: an integer when the count is odd, a
one-decimal float when the count is even.

## Examples

**Example 1** — alternates integer (odd count) and `.x` float (even count).
```
{"stream":[1,2,3,4]} → 1 1.5 2 2.5
```

**Example 2** — order of arrival is scrambled; the running median still tracks
the middle of everything seen so far.
```
{"stream":[5,15,1,3,2,8,7,9,10,6,11,4]} → 5 10.0 5 4.0 3 4.0 5 6.0 7 6.5 7 6.5
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: [LeetCode 295 — Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)
