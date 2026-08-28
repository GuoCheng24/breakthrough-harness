<!-- Place as .github/copilot-instructions.md or merge into yours.
     Full methodology: https://github.com/GuoCheng24/breakthrough-harness -->
# Research discipline (breakthrough-harness)

For any experiment or evaluation code in this repository:
- All method scoring goes through the single evaluation entry point; never
  compute metrics inline in experiment scripts.
- Null-model baselines (constant output, untrained model, input copy) are
  scored before any candidate; a well-scoring null model means the harness
  is broken - stop and fix it first.
- Metric data-range/convention is pinned in one place; if a published
  convention differs, report both, labelled.
- Hyperparameter tuning reads calibration data only; evaluation data is
  loaded only by the final confirmation step. Gains that do not reproduce
  on held-out data are not reported.
- Algorithm implementations exist exactly once, in a module; experiment
  scripts import them, never re-implement inline.
- New checks/tests must be demonstrated to fail on a deliberately broken
  input before they count, and must fail for the right reason.
- Numbers are persisted to files and committed before being quoted in text.
- Result summaries keep constructive claim polarity: the headline states what
  we propose/achieve and its number; audits and negative findings are
  supporting sections, never the headline.
