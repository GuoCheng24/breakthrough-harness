"""Generate the GitHub social-preview card (1200x630). Reproducible: python3 make_social_preview.py

The previous card was a screenshot of examples/toy_loop.py output. At the 360 px a Slack unfurl
gives a card, that was unreadable, so the message now lives in the headline and the terminal panel
is texture beside it. Layout shared with the other cards in this account via bin/lightcard.py.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path.home() / "bin"))
from lightcard import draw  # noqa: E402

out = draw(
    out=str(pathlib.Path(__file__).parent / "social-preview.png"),
    accent="#8957e5",
    badge="B",
    kicker="METHODOLOGY  ·  works with any agent stack",
    headline="The cheater tops the ranking",
    subline="and the held-out set executes it",
    body=["A candidate that secretly fits the calibration",
          "answers looks like a breakthrough for exactly",
          "as long as nobody checks it on files the",
          "tuning never touched. Nine agent stacks."],
    panel=[("$ python examples/toy_loop.py", "dim"),
           ("240.00 dB  CHEATER    -> held-out  -1.34", "red"),
           ("            COLLAPSED - calibration artifact", "red"),
           ("23.31 dB   ista 5e-2  -> held-out  22.31", "ok"),
           ("            REPRODUCED", "ok")],
    footer="github.com/GuoCheng24/breakthrough-harness",
)
print(f"written {pathlib.Path(out).name} 1200x630")
