# breakthrough-harness

[![checks](https://github.com/GuoCheng24/breakthrough-harness/actions/workflows/test.yml/badge.svg)](https://github.com/GuoCheng24/breakthrough-harness/actions/workflows/test.yml) [![license](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![deps](https://img.shields.io/badge/deps-numpy%20only-blue)](examples/toy_loop.py)

**Make your research agent hard to fool — starting with itself.**

[中文版](README.zh-CN.md) · works with any agent stack · pure methodology + one runnable demo

```text
calibration sweep (tuning allowed here only)          held-out confirmation (tuning never)
   240.00 dB  CHEATER    <- tops the ranking             CHEATER    240.00 ->  -1.34  COLLAPSED
    23.31 dB  ista 5e-2                                  ista 5e-2   23.31 ->  22.31  REPRODUCED
    16.99 dB  ista 2e-2                                  ista 2e-2   16.99 ->  14.87  REPRODUCED
    -0.00 dB  null: zeros  <- the floor, where it belongs
```

That is `python examples/toy_loop.py` (< 30 s, numpy only): a candidate that
secretly fits the calibration answers looks like a breakthrough, and the
held-out confirmation executes it. **This half screen is the entire
philosophy of the repository.**

Most agent harnesses teach an agent how to work. This one teaches a research
agent how **not to deceive itself** — because in research the failure mode is
rarely "the code crashed" and almost always "the number looked great and was
wrong." Every rule here was paid for by a real failure; none is hypothetical.
The repository follows its own rules: what these pages claim, `tests/` checks
on every push.

## The core claim

> **Breakthroughs are a throughput problem.**
> breakthrough ≈ many cheap attempts × a scoring function that cannot be fooled.

Serial, hand-crafted experiments produce a few dozen attempts per year; the
systems that actually produced constructive breakthroughs (program search
over mathematical constructions, tournament-style hypothesis engines) share
one skeleton: **parallel cheap generation + automated un-foolable selection**.
You cannot copy their compute; you can copy the skeleton — if the scoring
function is engineered with the rigor a referee would apply. That engineering
is this repository.

And a quieter corollary: when every attempt is expensive, the rational move
is to audit what exists rather than build what might fail — audits have
guaranteed deliverables. Teams that keep sliding into negative-result papers
are responding rationally to the price of an attempt. **Fix the price and the
sliding stops.**

## What is inside

| Directory | What it gives you |
|---|---|
| [`loop/`](loop/LOOP.md) | The breakthrough loop: generate-with-reasons → parallel sweep → select on calibration → **confirm on held-out** |
| [`harness/`](harness/CHECKLIST.md) | Building a scoring harness, incl. the **anti-cheat four**: null models on the floor; metric conventions pinned & double-reported; calibration/evaluation physically separated; absurd baseline ⇒ freeze everything |
| [`gates/`](gates/GATES.md) | Go/no-go gates: target triage, the **claim-polarity red line**, occupancy checks at claim level |
| [`rules/`](rules/RULES.md) | Ten engineering rules, **each ending with the real failure that paid for it** |
| [`examples/`](examples/) | The runnable demo above |
| [`adapters/`](adapters/) | Drop-ins for **your** stack — see below |

## Use it with your agent, whatever it is

The methodology is plain markdown — nothing here depends on any vendor. The
adapters just package it for wherever your agent reads instructions:

| Your stack | Do this |
|---|---|
| **Any tool reading `AGENTS.md`** — incl. **DeepSeek Harness** (its official agent instruction file *is* `AGENTS.md`), Codex, Cursor, Jules, Amp, … | copy [`adapters/AGENTS.md`](adapters/AGENTS.md) into your project root |
| **Claude Code** | `cp -r adapters/claude-code/breakthrough-loop ~/.claude/skills/` |
| **Cursor** | `cp adapters/cursor/breakthrough-loop.mdc your-project/.cursor/rules/` |
| **GitHub Copilot** | merge [`adapters/copilot/copilot-instructions.md`](adapters/copilot/copilot-instructions.md) into `.github/copilot-instructions.md` |
| **Anything else** (raw API, LangChain, custom loop, a human) | paste [`adapters/SYSTEM_PROMPT.md`](adapters/SYSTEM_PROMPT.md) |

## Quick start

```bash
git clone https://github.com/GuoCheng24/breakthrough-harness
cd breakthrough-harness
python examples/toy_loop.py     # < 30 s, numpy only
```

## The five habits, in one screen

1. **Null models first.** Before believing any score, ask what a method that
   learned nothing would score. If your pipeline can't tell them apart, fix
   the pipeline before running a single experiment.
2. **Calibration and evaluation never touch.** Tune on one set of files,
   report on another. A gain that does not survive the held-out set does not
   exist.
3. **A baseline you cannot beat is a recipe you have not finished reading.**
   Published baselines hide layers: the optimizer, the loss, the metric
   convention, the operator. Read until your reproduction matches.
4. **Claims have a polarity.** The main sentence of a result must be
   constructive — "we propose X, it solves Y, the number is Z." Audit output
   supports the claim; it is never the claim.
5. **Every guard must be shown to fail.** A check never seen firing on a
   deliberately broken input is decoration — guards in this very repository
   were caught silently passing before this rule existed.

## What this is, and is not

| | Orchestration frameworks | **breakthrough-harness** |
|---|---|---|
| Teaches the agent | how to work | how **not to fool itself** |
| Form | runtime / SDK | plain markdown + one numpy file |
| Lock-in | their stack | none — adapters for every stack |
| Guards | agent capability | **scientific validity** of what the agent reports |

It plugs into whatever you already run. It replaces nothing.

## License

MIT. Use it, fork it, disagree with it — but if a rule here saves you a
month, a star helps other people find it.
