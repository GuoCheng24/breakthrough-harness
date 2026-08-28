"""Generate the GitHub social-preview card (1280x640). Reproducible: python3 make_social_preview.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

W, H = 12.8, 6.4
fig = plt.figure(figsize=(W, H), dpi=100)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
ax.add_patch(plt.Rectangle((0, 0), W, H, color="#0d1117"))

SANS, MONO = "Liberation Sans", "Liberation Mono"
ax.text(0.75, 5.55, "breakthrough-harness", fontsize=34, fontweight="bold",
        color="#e6edf3", family=SANS)
ax.text(0.75, 4.92, "Make your research agent hard to fool - starting with itself.",
        fontsize=17, color="#8b949e", family=SANS)

# terminal card
card = FancyBboxPatch((0.72, 1.28), 11.36, 3.05, boxstyle="round,pad=0.12",
                      fc="#161b22", ec="#30363d", lw=1.5)
ax.add_patch(card)
ax.text(0.95, 4.02, "$ python examples/toy_loop.py", fontsize=13.5,
        color="#7d8590", family=MONO)
rows = [
    ("  240.00 dB  CHEATER    <- tops calibration", "#f85149",
     "   -> held-out  -1.34   COLLAPSED", "#f85149"),
    ("   23.31 dB  ista 5e-2", "#e6edf3", "   -> held-out  22.31   REPRODUCED", "#3fb950"),
    ("   -0.00 dB  null: zeros  <- the floor, where it belongs", "#58a6ff", "", ""),
]
y = 3.55
for left, cl, right, cr in rows:
    ax.text(0.95, y, left, fontsize=14.5, color=cl, family=MONO)
    if right:
        ax.text(6.85, y, right, fontsize=14.5, color=cr, family=MONO)
    y -= 0.52
ax.text(0.95, y - 0.05,
        "null models on the floor  |  calibration never touches held-out  |  every guard shown to fail",
        fontsize=12.5, color="#7d8590", family=MONO)

ax.text(0.75, 0.62, "9 agent stacks: AGENTS.md (DeepSeek Harness, OpenAI Codex) "
        "- Claude Code - Cursor - Copilot - Gemini - Windsurf - Cline - Aider",
        fontsize=12.5, color="#8b949e", family=SANS)
import pathlib; fig.savefig(pathlib.Path(__file__).parent / "social-preview.png")
print("written social-preview.png 1280x640")
