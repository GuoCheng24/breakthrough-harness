# Campaign starter template

A runnable skeleton of the discipline - adapt it to your task in roughly the
order below. Pure numpy; `python run_round.py` works as-is.

| File | What it is | What you change |
|---|---|---|
| `harness.py` | The only file that touches ground truth: entry point, tiers, null models, logged held-out access, freeze rule | Replace the toy problem + metric; keep the structure |
| `run_round.py` | One loop round: generate with reasons -> sweep -> select -> confirm -> ledger | Your candidates and reasons |
| `test_guards.py` | Guards, incl. one deliberate violation | Grow it: every failure you meet becomes a check |

Ground rules baked in: hyperparameter tuning reads calibration only; every
held-out access is appended to `heldout_access.jsonl`; results are persisted
to `ledger.jsonl` before you write sentences about them; a null model
scoring near the top halts everything.

Before round 1, add your Gate 1 numbers (see `../gates/GATES.md`): oracle
ceiling and trivial baseline through this same pipeline.
