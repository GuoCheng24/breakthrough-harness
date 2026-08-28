"""Generate the README terminal animation (demo.gif) from the demo's real
output. Reproducible: python3 make_demo_gif.py (pillow only)."""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
FONT = "/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf"
FONT_B = "/usr/share/fonts/liberation-mono/LiberationMono-Bold.ttf"

BG, FG, DIM = "#0d1117", "#e6edf3", "#7d8590"
RED, GREEN, BLUE, YELLOW = "#f85149", "#3fb950", "#58a6ff", "#d29922"

CMD = "$ python examples/toy_loop.py"
LINES = [  # (text, color) - the demo's real output, abridged to fit one screen
    ("================================================================", DIM),
    ("calibration sweep  (8 instances - tuning allowed here only)", FG),
    ("================================================================", DIM),
    ("   240.00 dB   CHEATER       (suspiciously good on calibration)", RED),
    ("    23.31 dB   ista 5e-2     (sparsity prior, strong)", FG),
    ("    16.99 dB   ista 2e-2     (sparsity prior, moderate)", FG),
    ("    16.42 dB   ista 2e-1     (over-sparse control)", FG),
    ("     5.00 dB   ridge 1e-2    (textbook default)", FG),
    ("    -0.00 dB   null: zeros   (anti-cheat floor)", BLUE),
    ("    -1.92 dB   null: A^T y   (anti-cheat floor, physics flavour)", BLUE),
    ("", FG),
    ("  anti-cheat: null models on the floor - where they belong", DIM),
    ("", FG),
    ("================================================================", DIM),
    ("held-out confirmation  (32 unseen instances, tuning never)", FG),
    ("================================================================", DIM),
    ("  CHEATER     calib 240.00 -> held-out  -1.34   COLLAPSED", RED),
    ("  ista 5e-2   calib  23.31 -> held-out  22.31   REPRODUCED", GREEN),
    ("  ista 2e-2   calib  16.99 -> held-out  14.87   REPRODUCED", GREEN),
    ("", FG),
    ("The cheater topped calibration and collapsed on held-out data.", YELLOW),
    ("That single comparison is why the two sets exist.", YELLOW),
]

W, PAD, LH, FS = 820, 24, 30, 18
H = PAD * 2 + LH * (len(LINES) + 2)
font = ImageFont.truetype(FONT, FS)
font_b = ImageFont.truetype(FONT_B, FS)


def frame(n_lines, cursor=False, cmd_chars=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):  # window dots
        d.ellipse([PAD + i * 26, 14, PAD + i * 26 + 13, 27], fill=c)
    cmd = CMD if cmd_chars is None else CMD[:cmd_chars]
    d.text((PAD, PAD + 14), cmd + ("_" if cursor else ""), font=font_b, fill=GREEN)
    for i in range(n_lines):
        text, color = LINES[i]
        bold = "CHEATER" in text or "REPRODUCED" in text
        d.text((PAD, PAD + 14 + LH * (i + 2)), text,
               font=font_b if bold else font, fill=color)
    return im


frames, durations = [], []
for k in range(0, len(CMD) + 1, 3):            # typing
    frames.append(frame(0, cursor=True, cmd_chars=k)); durations.append(45)
frames.append(frame(0)); durations.append(350)
for i in range(1, len(LINES) + 1):             # output reveal
    text = LINES[i - 1][0]
    frames.append(frame(i))
    slow = ("CHEATER" in text or "REPRODUCED" in text or "null" in text
            or "cheater" in text)
    durations.append(600 if slow else 120)
durations[-1] = 6000                           # hold the ending
frames[0].save(HERE / "demo.gif", save_all=True, append_images=frames[1:],
               duration=durations, loop=0, optimize=True)
print(f"demo.gif: {len(frames)} frames, {W}x{H}, "
      f"{(HERE / 'demo.gif').stat().st_size // 1024} KB")
