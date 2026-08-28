# Contributing

This repository holds itself to the rules it publishes. Contributions are
welcome under the same bar:

## Adding or changing a rule
- **A new rule must arrive with its tuition** — the real (anonymised)
  failure that paid for it. Hypothetical rules are declined; the repository's
  value is that none of its rules are hypothetical.
- `tests/test_claims.py` counts rules and tuition notes; extend it if your
  change adds a checkable claim anywhere in the pages.

## Changing the methodology text
- The five plain-markdown adapters are **generated** — edit
  `adapters/_core.md`, run `python adapters/build.py`, commit both. CI fails
  on drift.
- Every page claim that can be checked mechanically should be: if you write
  "every adapter contains X", add the assertion.

## Adding a guard or check
- Show it failing: break the thing it watches, watch it fire **for the right
  reason**, restore. Include that demonstration in the PR description.

## Disagreeing with a rule
Open an issue with the counter-example. A rule that survives a real
counter-example gets the counter-example added to its text; a rule that
does not survives gets amended. Both outcomes improve the repository.

## Ground rules
- No private paths, usernames, or unpublished results in any file — the
  sanitisation guard scans every text file.
- Runnable examples stay numpy-only and under a minute.
