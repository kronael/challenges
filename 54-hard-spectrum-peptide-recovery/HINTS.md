# Hints — 54 Hard — Spectrum Peptide Recovery

> Spoilers. Open only when stuck.

- Expand candidate peptides one mass at a time. Discard any candidate whose
  total already exceeds the parent mass, the largest spectrum value.
- Compute a candidate's linear spectrum before it closes into a cycle. Its mass
  multiset must be contained in the experimental spectrum multiset. Otherwise
  no extension can become a match.
- When a candidate reaches the parent mass, compare its complete cyclic spectrum
  with the input. Keep all matches long enough to choose the lexicographically
  smallest sequence.
- Use frequency maps. Spectrum multiplicity matters as much as membership.
- Enumerating every mass sequence up to the parent mass is correct but
  exponential. That unpruned search is the rotten reference.

Sources:

- [Chen et al. — A dynamic programming approach to de novo peptide sequencing](https://arxiv.org/abs/cs/0101016)
- [Bandeira et al. — Multi-spectra peptide sequencing](https://pubmed.ncbi.nlm.nih.gov/18785330/)
- [Ngoka and Gross — Sequencing cyclic peptides by mass spectrometry](https://doi.org/10.1016/S1044-0305(99)00049-5)
