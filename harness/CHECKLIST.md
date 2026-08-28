# Building a harness that cannot be fooled

The harness is the scoring engine the whole loop stands on. If it can be
fooled, parallel search will find the fooling faster than it finds the
breakthrough — automated selection amplifies whatever your metric actually
rewards, which is not always what you meant.

## The checklist

### Interface
- [ ] A "method" is a callable with a fixed signature. It receives inputs;
      **ground truth lives only inside the harness.**
- [ ] One evaluation entry point (a script or function) that everything —
      humans, agents, CI — calls identically. If two callers can score the
      same method differently, you have two harnesses and zero trust.

### Tiers (make attempts cheap without making them sloppy)
- [ ] **Tier 0, seconds**: shape, finiteness, value range. Catches candidates
      that never ran.
- [ ] **Tier 1, minutes**: a small fixed subset, the loop's workhorse.
- [ ] **Tier 2, hours**: full set, multiple seeds, secondary metrics. Only
      survivors come here.

### The anti-cheat four
- [ ] **Null models must score like null models.** A constant output, an
      untrained model, an input-copy — score them first. If the day comes
      when a null model's score improves, the harness is broken: freeze every
      conclusion and fix it before anything else. (Corollary: a candidate
      scoring absurdly *well* deserves the same freeze — see the cheater in
      `examples/toy_loop.py`, which posts 240 dB on calibration.)
- [ ] **Metric conventions pinned, and double-reported when they differ.**
      The same reconstruction scored 3 dB apart under two common PSNR
      data-range conventions; a published table is only comparable under its
      own convention. Report the official convention for comparison and a
      fixed convention for internal consistency, labelled.
- [ ] **Calibration and evaluation physically separated** — different files,
      different directories, ideally different loaders. "I'll just peek once"
      is how test-set tuning starts. The separation must be structural, not
      behavioral.
- [ ] **An absurd baseline score freezes everything.** When FBP scores below
      a constant image, the bug is in the harness, not in fifty years of
      tomography. The harness's own rule fired on its own author within the
      first hour of its existence; that is the rule working.

### Reference baselines
- [ ] Reproduce at least one **published** number before trusting any of your
      own. A baseline you cannot beat is a recipe you have not finished
      reading — one published TV baseline took seven layers to match
      (the optimizer wasn't the assumed one; the loss wasn't the assumed one;
      the metric convention, the regularizer weight scale, and finally the
      forward operator itself all differed). Every layer changed the number.
- [ ] Calibrate physical constants on **different data** than you evaluate
      on, and make the interface admit only scalars — so calibration cannot
      silently become per-sample fitting.

### Guards must be shown to fail
- [ ] Every check gets one deliberate violation test: break the thing it
      watches, watch it fire, restore. A guard never seen firing is
      decoration. Several guards in the repository this methodology comes
      from were themselves caught silently passing — including one whose
      "success" was an environment variable leaking into a child process.
- [ ] When verifying a guard by deliberate breakage, confirm it fails **for
      the right reason** — a test can go red because an unrelated assertion
      tripped first, and then it protects nothing.

## Feeding the harness

Every failure the loop encounters becomes a new check — the harness compounds
across rounds and across projects. A large lab's harness is built once and
frozen; yours gets sharper every time you are wrong, which — used correctly —
is your structural advantage over them.
