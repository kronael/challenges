# Hints — 21 KMP String Search

> Spoilers. Open only when stuck.

- **Failure function**: for each prefix of the pattern, precompute the length of
  the longest proper prefix that is also a suffix. On a mismatch this tells you
  how far to fall back inside the pattern instead of restarting from the top.
- **Linear matching**: scan the text once, advancing a pattern pointer; on a
  mismatch, fall back via the failure function rather than rewinding the text.
  The text pointer never moves backward, so matching is O(|T|+|P|). When the
  pattern pointer reaches the end, record a match and fall back to keep finding
  overlapping ones.
- **The related Z-function** answers "how far does the match extend from here"
  and solves the same problem in linear time if you prefer it.

The naive O(|T|·|P|) scan — try the pattern at every start position, comparing
character by character — is what `rotten/main.py` does. It is correct but
TIMEOUTs on the large cases.
