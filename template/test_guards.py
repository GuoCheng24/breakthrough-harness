"""Guards for the harness itself - each shown to fail before it counts."""
import subprocess
import sys
import pathlib

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from harness import NULLS, N_FEAT, evaluate, null_floor


def test_null_models_sit_on_the_floor():
    floor = null_floor()
    assert all(v < 3 for v in floor.values()), floor


def test_freeze_rule_fires_on_a_leaking_null():
    """Deliberate violation: register a null that secretly looks up the
    calibration ground truth (a leak), then watch the freeze rule halt the
    next honest evaluation - for the right reason."""
    import harness

    def leaking_null(A, y):
        for A2, y2, x2 in harness._CALIB:
            if y2.shape == y.shape and np.allclose(y2, y):
                return x2
        return np.zeros(N_FEAT)

    NULLS["null:leak"] = leaking_null
    try:
        evaluate(lambda A, y: np.linalg.pinv(A) @ y, "least-squares", "calibration")
    except SystemExit as e:
        assert "ANTI-CHEAT" in str(e)
    else:
        raise AssertionError("freeze rule did not fire on a truth-leaking null")
    finally:
        del NULLS["null:leak"]


def test_one_round_runs_end_to_end():
    r = subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "run_round.py")],
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr
    assert "REPRODUCED" in r.stdout and "null floor" in r.stdout
