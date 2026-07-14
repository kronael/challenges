# Hints — 49 Hard — Gene Region Decoder

> Spoilers. Open only when stuck.

- This is maximum-score decoding in a hidden Markov model. The scores can be
  treated as log probabilities, so multiplication becomes addition.
- For every sequence position and current state, keep the best score of a path
  ending there. Try every previous state when filling that value.
- Store the winning previous-state index for each cell. Start at the best final
  state and follow those indices backward to recover the path.
- The time cost is `O(n · k²)` for sequence length `n` and `k` states. Scores
  need only two rows, while path recovery needs `O(n · k)` predecessor entries.
- The rotten reference enumerates all `kⁿ` state paths. It is correct on the
  small cases and unusable on the benchmark cases.

Sources:

- FragGeneScan applies this model to coding-region prediction in noisy reads:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2978382/
- Rabiner's tutorial develops the decoding recurrence and backtracking:
  https://doi.org/10.1109/5.18626
