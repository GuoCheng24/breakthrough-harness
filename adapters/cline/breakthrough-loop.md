# Breakthrough-loop discipline (Cline rules)

Copy this file into `.clinerules/` in your project (or paste it into a single
`.clinerules` file). Full methodology: https://github.com/GuoCheng24/breakthrough-harness

## Research discipline for this project

### Target triage (before any experiment campaign)
Confirm all three, or say which one fails and stop:
1. a cheap scoring function exists (seconds–minutes, unambiguous, machine-run);
2. the groundwork exists (data downloadable, baselines published);
3. a win is externally recognisable (leaderboard, or referee-grade controlled
   comparison).

### Harness before methods
- One evaluation entry point; ground truth stays inside the harness.
- Score null models first (constant output, untrained model, input copy).
  If a null model ever scores well, the harness is broken: freeze all
  conclusions and repair it before anything else.
- Pin metric conventions; if the published convention differs from ours,
  report both, labelled.
- Calibration and evaluation data are physically separate; tuning of any
  kind touches calibration only.
- Reproduce one published baseline number before trusting our own. If we
  cannot match it, keep reading the recipe (optimizer, loss, metric
  convention, operator) — do not "improve" an unmatched baseline.
- Verify every new guard by breaking what it watches, and confirm it fails
  for the right reason.

### The loop
Generate 10–30 variants per round, each with a one-line reason it might win;
sanity-check one instance before entry; sweep in parallel with executors that
only call the entry point (never write method code inline); select on
calibration; confirm top-k on held-out at full budget. **A gain that does not
reproduce held-out does not exist.** Persist numbers to disk before writing
sentences about them; convert each round's failures into new harness checks.

### Claim polarity
The main sentence of any result must be constructive: "we propose X, it
solves Y, the number is Z." Audits, ablations and negative findings are
supporting material, never the headline. Check: is the main verb
"propose/solve/achieve", or "found that … fails"?

### Stop conditions
- Candidates stop carrying new reasons → the space is mined out: record the
  ceiling and move up a tier; do not keep sweeping it.
- Any anti-cheat check fires → fix the harness before interpreting anything.
