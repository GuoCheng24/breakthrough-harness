---
name: breakthrough-loop
description: >
  Run research as a breakthrough loop - parallel cheap candidate generation
  against an un-foolable scoring harness - instead of serial hand-crafted
  experiments. Use WHENEVER the user starts a method/algorithm research
  project, asks for a "breakthrough", "novel method", "beat the baseline /
  SOTA", or when experiments keep sliding into audits and negative results.
  Triggers: "突破", "创新方法", "beat baseline", "新算法", "breakthrough",
  "novel method", "win the benchmark".
---

# Breakthrough Loop

Drop this folder into your `.claude/skills/` and adapt the bracketed parts.
Full methodology: https://github.com/GuoCheng24/breakthrough-harness

## Before anything: target triage (all three or stop)
1. Cheap scoring function exists (seconds-minutes, unambiguous, machine-run)?
2. Groundwork exists (data downloadable, baselines published)?
3. A win is externally recognisable (leaderboard / referee-grade comparison)?

## Phase 1 — build the harness first (not the method)
- One evaluation entry point; ground truth stays inside the harness.
- Tiered scoring: Tier0 seconds (shape/finiteness) → Tier1 minutes (small
  subset) → Tier2 hours (full set, survivors only).
- Anti-cheat four: null models score first and must land on the floor;
  metric conventions pinned (double-report if the official one differs);
  calibration/evaluation data physically separated; an absurd baseline
  score freezes all conclusions.
- Reproduce one published baseline number before trusting your own. If you
  cannot match it, you have not finished reading the recipe - keep reading
  (optimizer, loss, metric convention, operator - every layer moves numbers).
- Verify every guard by breaking what it watches, and check it fails for
  the right reason.

## Phase 2 — the loop (one round per day)
1. Generate 10-30 variants, each with a one-line reason it might win;
   one-instance sanity check before entry.
2. Sweep in parallel (subagents/processes as *executors only* - they call
   the entry point, they never write method code).
3. Select on calibration data only.
4. Confirm top-k on held-out data at full budget. Unreproduced gains do not
   exist. Persist numbers to disk, commit, and convert this round's failure
   modes into new harness checks.

## Claim polarity (at proposal and at writing time)
The main sentence must be constructive: "we propose X, it solves Y, number
is Z." Audit output (ablations, robustness, honest scope) supports claims,
never is one. Check-sentence: is the main verb "propose/solve/achieve" or
"found that ... fails"?

## Stop conditions
- Candidates stop carrying new reasons → the space is mined out: record the
  ceiling, close it, move up a tier. Do not sweep a mined-out space.
- A null model's score improves → the harness broke: freeze conclusions,
  fix it first.
