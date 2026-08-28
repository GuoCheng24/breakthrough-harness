"""Generate the breakthrough-loop diagram. Reproducible: python3 make_loop_diagram.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BG, CARD, EDGE = "#0d1117", "#161b22", "#30363d"
FG, DIM, RED, GREEN, BLUE, YELLOW = "#e6edf3", "#8b949e", "#f85149", "#3fb950", "#58a6ff", "#d29922"
SANS = "Liberation Sans"

W, H = 8.2, 3.6
fig = plt.figure(figsize=(W, H), dpi=100)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
ax.add_patch(plt.Rectangle((0, 0), W, H, color=BG))

# held-out zone shading (right of the wall)
ax.add_patch(plt.Rectangle((6.05, 0.72), 2.15, 2.6, color="#101820"))
ax.plot([6.05, 6.05], [0.72, 3.32], color=YELLOW, lw=1.6, ls=(0, (5, 3)))
ax.text(6.02, 3.38, "tuning never crosses this line", fontsize=8.5, color=YELLOW,
        family=SANS, ha="center")

def box(x, y, w, h, title, sub, tc=FG):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.07",
                                fc=CARD, ec=EDGE, lw=1.2))
    ax.text(x + w / 2, y + h - 0.32, title, fontsize=10.5, color=tc,
            family=SANS, fontweight="bold", ha="center")
    ax.text(x + w / 2, y + 0.30, sub, fontsize=8.2, color=DIM, family=SANS,
            ha="center")

def arrow(x1, y1, x2, y2, color=DIM, style="-|>", lw=1.4, rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                 color=color, lw=lw, mutation_scale=13,
                 connectionstyle=f"arc3,rad={rad}"))

Y, BH = 2.18, 1.0
box(0.25, Y, 1.72, BH, "GENERATE", "10-30 variants,\neach with a reason")
box(2.22, Y, 1.72, BH, "SWEEP", "parallel executors,\nentry point only")
box(4.19, Y, 1.72, BH, "SELECT", "on calibration\ndata only")
box(6.22, Y, 1.72, BH, "CONFIRM", "top-k on held-out,\nfull budget", tc=YELLOW)
arrow(1.97, Y + BH / 2, 2.22, Y + BH / 2)
arrow(3.94, Y + BH / 2, 4.19, Y + BH / 2)
arrow(5.91, Y + BH / 2, 6.22, Y + BH / 2)

# outcomes
ax.text(7.94, 1.62, "REPRODUCED  ->  the claim", fontsize=9, color=GREEN,
        family=SANS, fontweight="bold", ha="right")
ax.text(7.94, 1.32, "COLLAPSED   ->  did not exist", fontsize=9, color=RED,
        family=SANS, fontweight="bold", ha="right")
arrow(7.08, Y - 0.02, 7.08, 1.74, color=DIM)

# harness base
ax.add_patch(FancyBboxPatch((0.25, 0.28), 5.66, 0.62, boxstyle="round,pad=0.07",
                            fc="#0f1a2b", ec=BLUE, lw=1.2))
ax.text(3.08, 0.59, "THE HARNESS   -   null models on the floor  |  pinned metrics  |  "
        "guards shown to fail", fontsize=8.8, color=BLUE, family=SANS,
        ha="center", fontweight="bold")
# failures feed back
arrow(6.6, 0.72, 5.95, 0.59, color=RED, rad=0.25)
ax.text(6.7, 0.42, "every failure becomes a new check", fontsize=8.2,
        color=RED, family=SANS, ha="center")
# harness underpins stages
for x in (1.11, 3.08, 5.05):
    arrow(x, 0.94, x, Y - 0.04, color="#233041", lw=1.1, style="-")

import pathlib
fig.savefig(pathlib.Path(__file__).parent / "loop-diagram.png")
print("loop-diagram.png written")
