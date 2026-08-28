# breakthrough-harness

**Make your research agent hard to fool — starting with itself.**

[中文版](README.zh-CN.md) · MIT · pure methodology + one runnable demo · no framework lock-in

Most agent harnesses teach an agent how to work. This one teaches a research
agent how **not to deceive itself** — because in research, the failure mode is
rarely "the code crashed" and almost always "the number looked great and was
wrong."

Every rule in this repository was paid for by a real failure. None of them is
hypothetical. The repository that follows its own rules: the numbers quoted in
this README are checked by `tests/` on every push.

## The core claim

> **Breakthroughs are a throughput problem.**
> breakthrough ≈ many cheap attempts × a scoring function that cannot be fooled.

Serial, hand-crafted experiments produce a few dozen attempts per year; the
systems that actually produced constructive breakthroughs (program-search over
math constructions, tournament-style hypothesis engines) all share one
skeleton: **parallel cheap generation + automated un-foolable selection**.
A solo researcher with one GPU cannot copy their scale — but can copy the
skeleton, if the scoring function is engineered with the same rigor a referee
would apply. That engineering is this repository.

## What is inside

| Directory | What it gives you |
|---|---|
| [`loop/`](loop/LOOP.md) | The breakthrough loop: generate-with-reasons → parallel sweep → select on calibration → **confirm on held-out** |
| [`harness/`](harness/CHECKLIST.md) | How to build a scoring harness, including the **anti-cheat four**: null models must score like null models; metric conventions pinned and double-reported; calibration/evaluation data physically separated; an absurd baseline score freezes all conclusions |
| [`gates/`](gates/GATES.md) | Go/no-go gates: the three-question target triage, the **claim-polarity red line** ("we propose X and it wins" vs "we audited X and it fails"), occupancy checks done at claim level |
| [`rules/`](rules/RULES.md) | Engineering rules with the tuition that bought each one |
| [`examples/`](examples/) | A self-contained toy run of the full loop — watch the harness catch a cheating candidate and a calibration-overfit gain, in seconds, pure numpy |
| [`skills/`](skills/) | A drop-in skill template for Claude Code (`.claude/skills/`) so your agent carries the loop into every session |

## Quick start

```bash
git clone https://github.com/GuoCheng24/breakthrough-harness
cd breakthrough-harness
python examples/toy_loop.py     # < 30 s, no dependencies beyond numpy
```

The demo runs one full turn of the loop on a synthetic sparse-recovery
problem: 12 candidate methods are scored in parallel on a calibration set; one
of them cheats (it secretly fits the calibration answers) and tops the
calibration ranking; the held-out confirmation demotes it to last place, and
the null models sit exactly where null models belong. That half page of output
is the entire philosophy of this repository.

## The five habits, in one screen

1. **Null models first.** Before believing any score, ask what a method that
   learned nothing would score. If your pipeline can't tell them apart, fix
   the pipeline before running a single experiment.
2. **Calibration and evaluation never touch.** Tune on one set of files,
   report on another. A gain that does not survive the held-out set does not
   exist.
3. **A baseline you cannot beat is a recipe you have not finished reading.**
   Published baselines hide layers: the optimizer, the loss, the metric
   convention, the operator. Read until your reproduction matches; only then
   are your improvements real.
4. **Claims have a polarity.** The main sentence of a result must be
   constructive — "we propose X, it solves Y, the number is Z." Audit output
   (ablations, robustness, honest scope) supports the claim; it is never the
   claim.
5. **Every guard must be shown to fail.** A check that was never seen to fire
   on a deliberately broken input is not a check — several of the guards in
   this repository were themselves caught silently passing before this rule
   existed.

## What this is not

Not an orchestration framework, not a wrapper around any model API, not a
benchmark. It is the missing discipline layer that plugs into whatever agent
stack you already run. If you use Claude Code, `skills/` drops straight in;
if you use anything else, `loop/`, `harness/`, `gates/` and `rules/` are
plain markdown and a numpy file.

## License

MIT. Use it, fork it, disagree with it — but if a rule here saves you a
month, a star helps other people find it.
