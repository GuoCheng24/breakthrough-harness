"""One round of the breakthrough loop. Run: python run_round.py

Generate with reasons -> sweep on calibration -> select -> confirm top-k on
held-out -> persist the ledger. Adapt the candidate list; keep the shape.
"""
import json
import pathlib

import numpy as np

from harness import evaluate, null_floor, N_FEAT

LEDGER = pathlib.Path(__file__).parent / "ledger.jsonl"


def ista(lam, n_iter=200):
    def fn(A, y):
        L = np.linalg.norm(A, 2) ** 2
        x = np.zeros(N_FEAT)
        for _ in range(n_iter):
            x = x - A.T @ (A @ x - y) / L
            x = np.sign(x) * np.maximum(np.abs(x) - lam / L, 0)
        return x
    return fn


# ---- phase 1: generate, each with a one-line reason ------------------------
CANDIDATES = {f"ista {lam:g}": (ista(lam), reason) for lam, reason in [
    (0.005, "weak prior, near least-squares"),
    (0.02,  "moderate sparsity"),
    (0.05,  "matches the true sparsity level"),
    (0.2,   "over-sparse control"),
]}

print("null floor:", {k: round(v, 2) for k, v in null_floor().items()})

# ---- phase 2+3: sweep on calibration, select ------------------------------
calib = {n: evaluate(fn, n, "calibration") for n, (fn, _) in CANDIDATES.items()}
ranked = sorted(calib, key=calib.get, reverse=True)
for n in ranked:
    print(f"  calib {calib[n]:7.2f} dB  {n}  ({CANDIDATES[n][1]})")

# ---- phase 4: confirm top-k on held-out (logged), persist before prose ----
rows = []
for n in ranked[:2]:
    h = evaluate(CANDIDATES[n][0], n, "heldout")
    verdict = "REPRODUCED" if h > calib[n] - 3 else "COLLAPSED"
    rows.append({"name": n, "reason": CANDIDATES[n][1],
                 "calib": round(calib[n], 2), "heldout": round(h, 2),
                 "verdict": verdict})
    print(f"  confirm {n}: {calib[n]:.2f} -> {h:.2f}  {verdict}")

with LEDGER.open("a") as f:
    f.write(json.dumps({"round": "adapt-me", "results": rows}) + "\n")
print(f"ledger appended: {LEDGER.name}")
