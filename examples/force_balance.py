"""A flat hyperparameter sweep is not evidence of insensitivity.

Rule 3 of rules/RULES.md, runnable. The trap: your data term is a *mean*
over measurements, your regulariser is a *sum* over features - so their
gradients live on scales a few orders of magnitude apart. Sweep the
regulariser weight over four decades in the "textbook" range and every value
gives the same score: the sweep looks flat, the parameter looks inert.

It is not inert. Every value you tried was on the same side of the balance
point. Act 2 measures the force balance - one gradient-norm evaluation at the
starting point - and tells you where the real range is. Act 3 sweeps there
and finds a clean peak.

Pure numpy, seconds. The tuition behind this file: a real regulariser weight
was once swept across four decades with zero effect, and the balance point
sat three decades below the sweep floor.
"""
import numpy as np

rng = np.random.default_rng(0)
N_FEAT, N_MEAS, K_SPARSE, NOISE = 60, 40, 6, 0.05


def make_instance(rng):
    A = rng.standard_normal((N_MEAS, N_FEAT)) / np.sqrt(N_MEAS)
    x = np.zeros(N_FEAT)
    x[rng.choice(N_FEAT, K_SPARSE, replace=False)] = rng.standard_normal(K_SPARSE) * 2
    return A, A @ x + NOISE * rng.standard_normal(N_MEAS), x


INSTANCES = [make_instance(rng) for _ in range(8)]


def solve(A, y, lam, n_iter=300):
    """ISTA on  mean-squared data term + lam * sum-|x|  (the scale trap)."""
    L = np.linalg.norm(A, 2) ** 2 * 2 / N_MEAS
    x = np.zeros(N_FEAT)
    for _ in range(n_iter):
        g = 2 * A.T @ (A @ x - y) / N_MEAS            # mean over measurements
        x = x - g / L
        x = np.sign(x) * np.maximum(np.abs(x) - lam / L, 0)   # sum over features
    return x


def score(lam):
    errs = [np.linalg.norm(solve(A, y, lam) - x) / np.linalg.norm(x)
            for A, y, x in INSTANCES]
    return -20 * np.log10(max(float(np.mean(errs)), 1e-12))


def main():
    print("=" * 64)
    print("Act 1 - the textbook sweep (four decades)")
    print("=" * 64)
    for lam in (0.1, 1.0, 10.0, 100.0):
        print(f"  lam = {lam:6.1f}   score {score(lam):7.2f} dB")
    print("  -> essentially flat. A lazy conclusion: 'the regulariser does not matter'.")

    print()
    print("=" * 64)
    print("Act 2 - measure the force balance (one gradient evaluation)")
    print("=" * 64)
    A, y, _ = INSTANCES[0]
    g_data = np.linalg.norm(2 * A.T @ y / N_MEAS)      # data-term gradient at x=0
    g_reg = np.sqrt(N_FEAT)                            # ||sign(x)|| scale of sum-L1
    lam_star = g_data / g_reg
    print(f"  ||grad data||(0) = {g_data:.4f}     ||grad reg|| scale = {g_reg:.2f}")
    for lam in (0.1, 1.0, 10.0, 100.0):
        print(f"  lam = {lam:6.1f}   reg/data force ratio = {lam * g_reg / g_data:10.1f}x")
    print(f"  -> every tested value crushed the data term; the balance point sits")
    print(f"     near lam* ~ {lam_star:.4f}, below the sweep floor - the sweep never")
    print("     crossed it. (In the real incident this file anonymises, the gap")
    print("     was three full decades; here the toy keeps it small enough to see.)")

    print()
    print("=" * 64)
    print("Act 3 - sweep around the measured balance point")
    print("=" * 64)
    best = None
    for mult in (0.1, 0.3, 1.0, 3.0, 10.0):
        lam = lam_star * mult
        s = score(lam)
        tag = ""
        if best is None or s > best[1]:
            best, tag = (lam, s), "   <- peak"
        print(f"  lam = {lam:8.4f}   score {s:7.2f} dB{tag}")
    print(f"\n  A clean interior peak at lam = {best[0]:.4f} - the parameter was")
    print("  never inert; the sweep was simply on one side of the balance point.")
    print("  Cost of finding out: one gradient-norm evaluation.")


if __name__ == "__main__":
    main()
