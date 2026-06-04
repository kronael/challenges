# Hints — 43 Max Drawdown

> Spoilers. Open only when stuck.

- **Single left-to-right scan tracking the running peak**: walk the prices once,
  keeping `peak` = the maximum price seen so far (including the current day). For
  each day, the deepest drop that can end here is `peak - price[j]`. Take the
  maximum of that quantity over all days. That is O(n) time, O(1) extra space.
- **Why the running peak is the right peak**: the best `i` to pair with a trough
  at `j` is always the highest price at or before `j` — a higher earlier peak can
  only make the drop bigger. So you never need to look back over all earlier days;
  the running maximum already remembers the best one.
- **The trap — don't pair global max with global min blindly**: `max(prices) -
  min(prices)` is wrong when the minimum occurs *before* the maximum (e.g.
  `[1, 100]` has drawdown 0, not 99). The ordering constraint `i < j` is the whole
  point; the running-peak scan respects it for free.
- **Floor at zero**: initialise the answer to `0` so a strictly non-decreasing
  series correctly reports no drawdown.

The naive O(n²) approach (`max(prices[i] - prices[j] for i in range(n) for j in
range(i+1, n))`) is what `rotten/main.py` does — correct but it TIMEOUTs on the
large cases.
