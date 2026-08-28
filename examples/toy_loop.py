"""One full turn of the breakthrough loop, on a problem small enough to read.

Task: recover a sparse vector x from noisy measurements y = A x + noise.
Candidates: 12 configurations of classical estimators (with reasons attached).
Among them hides one CHEATER that secretly regresses toward the calibration
ground truth - the exact failure mode of tuning on your test set.

What the harness demonstrates, in order:
  1. null models score like null models (if they didn't, we would stop here);
  2. the cheater tops the CALIBRATION ranking - looking exactly like a
     breakthrough;
  3. the held-out confirmation demotes it to last place, while honest gains
     survive with roughly their calibration margin.

Pure numpy. Runs in seconds. No seeds were tuned to make the story work:
change SEED and the same qualitative story repeats, because it is structural.
"""
import os

import numpy as np

SEED = int(os.environ.get("SEED", "0"))
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- problem --
N_FEAT, N_MEAS, K_SPARSE, NOISE = 60, 40, 6, 0.05


def make_instance(rng):
    A = rng.standard_normal((N_MEAS, N_FEAT)) / np.sqrt(N_MEAS)
    x = np.zeros(N_FEAT)
    idx = rng.choice(N_FEAT, K_SPARSE, replace=False)
    x[idx] = rng.standard_normal(K_SPARSE) * 2
    y = A @ x + NOISE * rng.standard_normal(N_MEAS)
    return A, y, x


CALIB = [make_instance(rng) for _ in range(8)]      # tune here, and only here
HELDOUT = [make_instance(rng) for _ in range(32)]   # report here, tune never


# -------------------------------------------------------------- estimators --
def ridge(lam):
    def est(A, y):
        n = A.shape[1]
        return np.linalg.solve(A.T @ A + lam * np.eye(n), A.T @ y)
    return est


def ista(lam, n_iter=200):
    def est(A, y):
        L = np.linalg.norm(A, 2) ** 2
        x = np.zeros(A.shape[1])
        for _ in range(n_iter):
            x = x - (1 / L) * A.T @ (A @ x - y)
            x = np.sign(x) * np.maximum(np.abs(x) - lam / L, 0)
        return x
    return est


def cheater():
    """Nearest calibration ground truth, dressed up as an estimator.

    It never generalises - it has memorised the calibration answers. On the
    calibration set it is unbeatable; on anything else it is noise. This is
    what "tuning on the test set" looks like when it wears a lab coat.
    """
    def est(A, y):
        best, best_r = None, np.inf
        for Ac, yc, xc in CALIB:
            r = np.linalg.norm(A @ xc - y)
            if r < best_r:
                best, best_r = xc, r
        return best
    return est


# ------------------------------------------------------------- null models --
def null_zeros():
    return lambda A, y: np.zeros(N_FEAT)


def null_backproj():
    return lambda A, y: A.T @ y            # physically motivated but learns nothing


CANDIDATES = {
    # name: (estimator, one-line reason - every candidate must carry one)
    "ridge 1e-3":  (ridge(1e-3),  "smallest bias, if noise were tiny"),
    "ridge 1e-2":  (ridge(1e-2),  "textbook default"),
    "ridge 1e-1":  (ridge(1e-1),  "heavier shrinkage for this noise level"),
    "ridge 1.0":   (ridge(1.0),   "over-shrunk control"),
    "ista 5e-3":   (ista(5e-3),   "sparsity prior matches the truth, weak"),
    "ista 2e-2":   (ista(2e-2),   "sparsity prior, moderate"),
    "ista 5e-2":   (ista(5e-2),   "sparsity prior, strong"),
    "ista 2e-1":   (ista(2e-1),   "over-sparse control"),
    "CHEATER":     (cheater(),    "suspiciously good on calibration"),
    "null: zeros": (null_zeros(), "anti-cheat floor - must lose to everything real"),
    "null: A^T y": (null_backproj(), "anti-cheat floor with physics flavour"),
    "ridge 3e-2":  (ridge(3e-2),  "between the two best ridges"),
}


def score(est, instances):
    """Mean relative recovery error -> PSNR-like dB (higher is better)."""
    errs = []
    for A, y, x in instances:
        xh = est(A, y)
        errs.append(np.linalg.norm(xh - x) / max(np.linalg.norm(x), 1e-12))
    m = float(np.mean(errs))
    return -20 * np.log10(max(m, 1e-12))


def main():
    print("=" * 64)
    print("calibration sweep  (8 instances - tuning allowed here only)")
    print("=" * 64)
    calib = {n: score(e, CALIB) for n, (e, _) in CANDIDATES.items()}
    ranked = sorted(calib.items(), key=lambda kv: -kv[1])
    for name, s in ranked:
        note = CANDIDATES[name][1]
        print(f"  {s:7.2f} dB   {name:12s}  ({note})")

    nulls = [calib["null: zeros"], calib["null: A^T y"]]
    honest = [s for n, s in calib.items()
              if not n.startswith("null") and n != "CHEATER"]
    if max(nulls) >= max(honest) - 3:
        raise SystemExit("ANTI-CHEAT FIRED: a null model scores within 3 dB of "
                         "the best honest candidate - freeze every conclusion "
                         "and repair the harness before proceeding")
    print(f"\n  anti-cheat: null models at {nulls[0]:.2f} / {nulls[1]:.2f} dB - "
          "the floor is where it belongs")

    top3 = [n for n, _ in ranked[:3]]
    print("\n" + "=" * 64)
    print(f"held-out confirmation  (32 unseen instances) for top-3: {top3}")
    print("=" * 64)
    for name in top3:
        h = score(CANDIDATES[name][0], HELDOUT)
        delta = h - calib[name]
        verdict = "REPRODUCED" if delta > -3 else "COLLAPSED - calibration artifact"
        print(f"  {name:12s}  calib {calib[name]:7.2f} -> held-out {h:7.2f}   {verdict}")

    print("\nThe cheater topped calibration and collapsed on held-out data.")
    print("That single comparison is the entire reason the two sets exist.")


if __name__ == "__main__":
    main()
