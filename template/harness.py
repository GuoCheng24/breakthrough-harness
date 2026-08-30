"""The scoring harness - the only file allowed to touch ground truth.

Replace the toy problem with your task; keep the structure:
- one entry point (evaluate), tiers, null models registered first;
- calibration / held-out physically separate, held-out access LOGGED;
- the freeze rule runs on every call.
"""
import json
import pathlib
import time

import numpy as np

# ---- the toy problem (REPLACE with your task) ------------------------------
_rng = np.random.default_rng(7)
N_FEAT, N_MEAS, NOISE = 50, 35, 0.05


def _make_split(n, seed):
    """One entry per unit of independence (here: instance; for you: patient,
    speaker, site...). Never let two records of the same unit cross splits."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        A = rng.standard_normal((N_MEAS, N_FEAT)) / np.sqrt(N_MEAS)
        x = np.zeros(N_FEAT)
        x[rng.choice(N_FEAT, 5, replace=False)] = rng.standard_normal(5)
        out.append((A, A @ x + NOISE * rng.standard_normal(N_MEAS), x))
    return out


_CALIB = _make_split(8, seed=101)      # tuning allowed here only
_HELDOUT = _make_split(32, seed=202)   # confirmation only, access is logged

# ---- null models: scored first, pinned to the floor ------------------------
NULLS = {
    "null:zeros": lambda A, y: np.zeros(N_FEAT),
    "null:ATy":   lambda A, y: A.T @ y,
}

_ACCESS_LOG = pathlib.Path(__file__).parent / "heldout_access.jsonl"
_BEST_HONEST = -1e9


def _score_on(fn, data):
    errs = [float(np.linalg.norm(fn(A, y) - x) / max(np.linalg.norm(x), 1e-12))
            for A, y, x in data]
    return -20 * float(np.log10(max(float(np.mean(errs)), 1e-12)))


def evaluate(fn, name, split="calibration", tier=1):
    """The single entry point. Experiment scripts call this; nothing else."""
    if split == "heldout":
        with _ACCESS_LOG.open("a") as f:       # every access leaves a trace
            f.write(json.dumps({"t": time.time(), "name": name}) + "\n")
        data = _HELDOUT
    else:
        data = _CALIB if tier >= 1 else _CALIB[:2]
    score = _score_on(fn, data)
    # freeze rule: if the null floor ever rises to within 1 dB of the best
    # honest candidate seen, the harness is leaking - halt everything
    if split == "calibration" and not name.startswith("null:"):
        global _BEST_HONEST
        _BEST_HONEST = max(_BEST_HONEST, score)
        floor = max(_score_on(nf, data) for nf in NULLS.values())
        if floor >= _BEST_HONEST - 1:
            raise SystemExit(f"ANTI-CHEAT: null floor {floor:.2f} within 1 dB "
                             f"of best honest {_BEST_HONEST:.2f} - a null "
                             "model is scoring like a method; freeze and repair")
    return score


def null_floor(split="calibration"):
    data = _CALIB if split == "calibration" else _HELDOUT
    return {n: _score_on(f, data) for n, f in NULLS.items()}
