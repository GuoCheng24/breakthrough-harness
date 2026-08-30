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
    nulls = [float(x) for x in re.findall(r"null models at (-?[\d.]+) / (-?[\d.]+) dB", out)[0]]
    top = float(re.search(r"^\s*(-?[\d.]+) dB", out, re.M).group(1))
    assert max(nulls) < top - 3, "null models are not clearly below the top candidate"


def test_story_is_structural_not_seed_tuned():
    """toy_loop.py claims no seed tuning: any seed must repeat the story."""
    import os
    for seed in ("1", "2"):
        env = dict(os.environ, SEED=seed)
        r = subprocess.run([sys.executable, str(ROOT / "examples" / "toy_loop.py")],
                           capture_output=True, text=True, timeout=300, env=env)
        assert r.returncode == 0, r.stderr
        assert re.search(r"CHEATER.*COLLAPSED", r.stdout), f"seed {seed}: cheater survived"
        assert r.stdout.count("REPRODUCED") >= 2, f"seed {seed}: honest gains lost"


def test_anti_cheat_freeze_rule_actually_fires():
    """Habit 5 applied to the flagship demo itself: boost a null model to the
    top and the freeze rule must halt the script - for the right reason."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "toy_loop_broken", ROOT / "examples" / "toy_loop.py")
    tl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tl)
    reason, note = tl.CANDIDATES["CHEATER"][0], "deliberately broken null"
    tl.CANDIDATES["null: zeros"] = (reason, note)
    import pytest
    with pytest.raises(SystemExit, match="ANTI-CHEAT FIRED"):
        tl.main()


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
    """The sanitisation rule, enforced: no local paths, usernames, or session
    artifacts anywhere. Patterns are assembled at runtime so this file does
    not itself publish the tokens it hunts; every text file is scanned."""
    user = "".join(["chen", "gguo"])
    sess = "".join(["df19", "028c"])
    patterns = ["/" + "public/" + "home/", "/" + "public/" + "share/",
                user, sess, r"\[\[[a-z0-9-]+\]\]"]
    bad = []
    for doc in ROOT.rglob("*"):
        if doc.is_dir() or ".git" in doc.parts or doc.suffix == ".png":
            continue
        raw = doc.read_bytes()
        if b"\x00" in raw[:1024]:
            continue                      # binary
        text = raw.decode("utf-8", errors="ignore")
        if doc.name == "test_claims.py":
            continue                      # assembles the patterns above
        for pat in patterns:
            if re.search(pat, text):
                bad.append(f"{doc.relative_to(ROOT)}: matches a private pattern")
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
                ROOT / "adapters" / "claude-code" / "breakthrough-loop" / "SKILL.md",
                ROOT / "adapters" / "gemini" / "GEMINI.md",
                ROOT / "adapters" / "windsurf" / "breakthrough-loop.md",
                ROOT / "adapters" / "cline" / "breakthrough-loop.md",
                ROOT / "adapters" / "aider" / "CONVENTIONS.md"]
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
                     "adapters/claude-code/breakthrough-loop",
                     "adapters/gemini/GEMINI.md",
                     "adapters/windsurf/breakthrough-loop.md",
                     "adapters/cline/breakthrough-loop.md",
                     "adapters/aider/CONVENTIONS.md"):
            assert path in text, f"{name} does not mention {path}"


def test_force_balance_demo_tells_its_story():
    """Act 1 near-flat, Act 3 finds an interior peak well above Act 1's best."""
    r = subprocess.run([sys.executable, str(ROOT / "examples" / "force_balance.py")],
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "essentially flat" in out and "<- peak" in out
    assert "interior peak" in out, "demo no longer finds an interior peak"
    act1 = [float(m) for m in re.findall(r"lam =\s+[\d.]+\s+score\s+(-?[\d.]+) dB",
                                         out.split("Act 2")[0])]
    peak = max(float(m) for m in re.findall(r"score\s+(-?[\d.]+) dB(?=\s+<- peak)", out))
    assert peak > max(act1) + 10, f"peak {peak} not clearly above flat sweep {max(act1)}"


def test_generated_adapters_do_not_drift():
    """Five adapters are generated from adapters/_core.md; hand-edits drift."""
    r = subprocess.run([sys.executable, str(ROOT / "adapters" / "build.py"), "--check"],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr


def test_readme_visuals_exist_and_are_generated():
    """Both READMEs embed the demo gif and loop diagram; the assets and their
    reproducible generators must exist."""
    for name in ("README.md", "README.zh-CN.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert ".github/assets/demo.gif" in text, f"{name} missing demo.gif"
        assert ".github/assets/loop-diagram.png" in text, f"{name} missing diagram"
    for asset in ("demo.gif", "loop-diagram.png", "make_demo_gif.py",
                  "make_loop_diagram.py", "social-preview.png",
                  "make_social_preview.py"):
        assert (ROOT / ".github" / "assets" / asset).exists(), f"missing {asset}"


def test_template_is_actually_runnable():
    """The campaign starter must run a full round and pass its own guards."""
    tpl = ROOT / "template"
    r = subprocess.run([sys.executable, str(tpl / "run_round.py")],
                       capture_output=True, text=True, timeout=300, cwd=tpl)
    assert r.returncode == 0 and "REPRODUCED" in r.stdout, r.stderr
    r = subprocess.run([sys.executable, "-m", "pytest", "test_guards.py", "-q"],
                       capture_output=True, text=True, timeout=300, cwd=tpl)
    assert r.returncode == 0, r.stdout + r.stderr
    for junk in ("heldout_access.jsonl", "ledger.jsonl"):
        (tpl / junk).unlink(missing_ok=True)
