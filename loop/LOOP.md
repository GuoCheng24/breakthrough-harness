# The breakthrough loop

## Why a loop at all

A researcher running serial, hand-crafted experiments produces a few dozen
attempts per year. Every system that has actually produced constructive
breakthroughs — program search over mathematical constructions, tournament
hypothesis engines — shares one skeleton regardless of scale:

> **parallel cheap generation → automated un-foolable selection → survivors evolve**

You cannot copy their compute. You can copy the skeleton. What makes it work
at solo scale is not the parallelism — it is that **the cost of one attempt
drops from days to seconds**, which changes what "trying things" means.

There is a second, quieter reason. When every attempt is expensive, the
rational move is always to audit what exists rather than build what might
fail — auditing has a guaranteed deliverable, building does not. Teams that
"keep sliding into negative-result papers" are not undisciplined; they are
responding rationally to the price of an attempt. **Fix the price and the
sliding stops.**

## The four phases

### 1. Generate — with reasons, never at random
Each round: 10–30 candidate variants. Every candidate carries a one-line
reason it might win ("second-order penalty handles smooth gradients that
first-order staircases on"). No reason, no entry. At solo scale you cannot
afford random mutation; the reasons are your prior, and they compound —
losing reasons teach as much as winning ones.

Run a one-instance sanity check before a candidate enters the pool. A
candidate that NaNs on one example wastes a whole parallel slot.

### 2. Sweep — in parallel, executors only
Parallel agents (or processes) run the candidates. **Executors execute.**
They call a fixed evaluation entry point; they do not write or modify method
code. Variants are implemented and sanity-checked in the main loop first —
an agent improvising algorithm code inside a sweep is how silent sign flips
enter your results.

### 3. Select — on calibration data only
Rank on the calibration set. Tuning of any kind (hyperparameters, thresholds,
prompt wording) touches calibration data only. The evaluation set does not
exist during this phase.

### 4. Confirm — on held-out data, or it didn't happen
Top-k candidates re-score on the evaluation set at full budget.
**A gain that does not reproduce there does not exist** — write the collapsed
ones down too; a collapse is information about your calibration set.

Then: persist the numbers to disk, commit, and feed every failure mode you
met back into the harness as a new check. The harness must get harder to fool
every round.

## Cadence and roles

- One full round should fit in a day, most of it wall-clock waiting.
- The human sets the target, reads each round's top-3, and audits the harness
  itself. The human does not hand-review every candidate — that is the old
  expensive loop wearing a new hat.
- Stop condition: when a round's best candidates stop carrying *new reasons*
  (you are re-rolling the same dice), the space is mined out. Close it,
  write the ceiling number down, and move up a tier. Continuing to sweep a
  mined-out space is the comfort zone in a new shape.
