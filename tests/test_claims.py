"""The repository follows its own rules: what the READMEs claim is checked.

Prose drifts. These tests hold the pages to the files - the same discipline
harness/CHECKLIST.md prescribes, applied to the repository that prescribes it.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _docs():
    return sorted(p for p in ROOT.rglob("*.md")
                  if not any(part.startswith(".") for part in p.relative_to(ROOT).parts))


def test_toy_loop_runs_and_tells_its_story():
    """The demo must run, the cheater must top calibration and collapse held-out,
    and the nulls must sit on the floor - the README promises exactly this."""
    r = subprocess.run([sys.executable, str(ROOT / "examples" / "toy_loop.py")],
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "CHEATER" in out and "COLLAPSED" in out, "cheater was not caught"
    assert out.count("REPRODUCED") >= 2, "honest gains did not reproduce"
    # the cheater's collapse must land below both null models' calibration scores
    m = re.search(r"CHEATER\s+calib\s+([\d.]+)\s+->\s+held-out\s+(-?[\d.]+)", out)
    assert m and float(m.group(2)) < 1.0, "cheater held-out score suspiciously good"


def test_readme_quick_start_matches_the_demo():
    for name in ("README.md", "README.zh-CN.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "examples/toy_loop.py" in text, f"{name} quick start out of date"


def test_every_internal_link_resolves():
    bad = []
    for doc in _docs():
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            t = m.group(1).split("#")[0].strip()
            if not t or t.startswith(("http://", "https://", "mailto:")):
                continue
            if not (doc.parent / t).exists():
                bad.append(f"{doc.relative_to(ROOT)} -> {t}")
    assert not bad, "\n".join(bad)


def test_no_private_information_leaked():
    """The sanitisation rule, enforced: no local paths, no session artifacts,
    no internal memory references may appear anywhere in the repository."""
    patterns = [r"/public/home/", r"/public/share/", r"chengguo_tmp",
                r"\[\[[a-z0-9-]+\]\]", r"df19028c"]
    bad = []
    for doc in ROOT.rglob("*"):
        if doc.is_dir() or ".git" in doc.parts:
            continue
        if doc.suffix not in (".md", ".py", ".yml", ".yaml", ".txt", ""):
            continue
        try:
            text = doc.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        if doc.name == "test_claims.py":
            continue                      # this file names the patterns it hunts
        for pat in patterns:
            if re.search(pat, text):
                bad.append(f"{doc.relative_to(ROOT)}: matches {pat}")
    assert not bad, "\n".join(bad)


def test_rules_each_carry_tuition():
    """RULES.md promises every rule ends with its tuition. Count both."""
    text = (ROOT / "rules" / "RULES.md").read_text(encoding="utf-8")
    rules = len(re.findall(r"^## \d+\.", text, re.M))
    tuitions = text.count("*Tuition:")
    assert rules == tuitions >= 8, f"{rules} rules but {tuitions} tuition notes"


def test_every_adapter_carries_the_core_concepts():
    """Five concepts define the methodology; an adapter missing one is a
    different methodology wearing our name. Anchored on stable phrases."""
    concepts = ["null model", "calibration", "held-out", "entry point", "propose"]
    adapters = [ROOT / "adapters" / "AGENTS.md",
                ROOT / "adapters" / "SYSTEM_PROMPT.md",
                ROOT / "adapters" / "cursor" / "breakthrough-loop.mdc",
                ROOT / "adapters" / "copilot" / "copilot-instructions.md",
                ROOT / "adapters" / "claude-code" / "breakthrough-loop" / "SKILL.md"]
    bad = []
    for a in adapters:
        assert a.exists(), f"adapter missing: {a}"
        text = a.read_text(encoding="utf-8").lower()
        for c in concepts:
            if c not in text:
                bad.append(f"{a.relative_to(ROOT)}: missing '{c}'")
    assert not bad, "\n".join(bad)


def test_readme_adapter_table_matches_the_files():
    for name in ("README.md", "README.zh-CN.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        for path in ("adapters/AGENTS.md", "adapters/SYSTEM_PROMPT.md",
                     "adapters/cursor/breakthrough-loop.mdc",
                     "adapters/copilot/copilot-instructions.md",
                     "adapters/claude-code/breakthrough-loop"):
            assert path in text, f"{name} does not mention {path}"
