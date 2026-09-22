"""Generate the GitHub social-preview card (1200x630). Reproducible: python3 make_social_preview.py

The demo is the argument, so the card is the demo's result: three candidates, what each scored
on calibration, and what each scored on files the tuning never touched. The cheater's line is
the point, and a line that falls off a cliff is legible at any size.

Numbers come from running examples/toy_loop.py, not from literals: the demo is numpy-only and
deterministic, and tests/test_claims.py already asserts this story holds.
"""
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cardkit import SANS, card  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
out_txt = subprocess.run([sys.executable, "examples/toy_loop.py"], cwd=ROOT,
                         capture_output=True, text=True, timeout=300).stdout
ROWS = []
for line in out_txt.splitlines():
    m = re.match(r"\s+(\S.*?)\s+calib\s+([-\d.]+)\s+->\s+held-out\s+([-\d.]+)", line)
    if m:
        ROWS.append((m.group(1).strip(), float(m.group(2)), float(m.group(3))))
if len(ROWS) < 3:
    raise SystemExit(f"toy_loop.py no longer prints the held-out table:\n{out_txt[-600:]}")


def chart(ax, accent):
    """A slope per candidate, calibration to held out.

    The cheater's calibration score is 240 dB, two orders of magnitude off anything real, so
    clamping it to the top of the scale is the honest way to show it - and the clamp is
    labelled rather than silent. Clamping without a label put its name on top of the next
    candidate's at 57% overlap, which sciglyph's checker caught.
    """
    xa, xb = 5.55, 9.05
    lo, hi = -3.0, 27.0

    def Y(v):
        return 1.28 + 2.00 * (min(max(v, lo), hi) - lo) / (hi - lo)

    ax.text(xa, 3.76, "calibration", fontsize=34, color="#55585c", family=SANS, ha="center")
    ax.text(xb, 3.76, "held out", fontsize=34, color="#55585c", family=SANS, ha="center")
    for name, calib, held in ROWS:
        cheat = held < 0
        colour = "#cf222e" if cheat else "#1a7f37"
        y0 = 3.44 if calib > hi else Y(calib)          # off-scale scores ride above the axis
        ax.plot([xa, xb], [y0, Y(held)], color=colour, lw=5, zorder=3, solid_capstyle="round")
        ax.plot([xa, xb], [y0, Y(held)], "o", ms=14, color=colour, zorder=4)
        label = f"CHEATER  {calib:.0f}" if calib > hi else name
        ax.text(xa - 0.24, y0, label, fontsize=34,
                fontweight="bold" if cheat else "normal",
                color=colour if cheat else "#55585c", family=SANS, ha="right", va="center")
        ax.text(xb + 0.26, Y(held), f"{held:.1f}", fontsize=36, fontweight="bold",
                color=colour, family=SANS, va="center")


out = card(
    out=str(pathlib.Path(__file__).parent / "social-preview.png"),
    accent="#8957e5", badge="B",
    kicker="METHODOLOGY  ·  works with any agent stack",
    headline="The cheater tops the ranking",
    evidence="dB on calibration, then on files tuning never touched",
    chart=chart,
    footer="github.com/GuoCheng24/breakthrough-harness",
    headline_size=46,
)
print(f"written {pathlib.Path(out).name}  " + "  ".join(f"{n} {c}->{h}" for n, c, h in ROWS))
