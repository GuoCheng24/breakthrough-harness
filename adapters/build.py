"""Generate the byte-identical adapter family from adapters/_core.md.

The methodology lives once, in _core.md; each stack gets a thin header in the
format its tool expects. Run `python adapters/build.py` to regenerate,
`python adapters/build.py --check` to verify nothing drifted (CI does this).
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CORE = (HERE / "_core.md").read_text(encoding="utf-8")
URL = "https://github.com/GuoCheng24/breakthrough-harness"

TARGETS = {
    "AGENTS.md": f"""<!--
  breakthrough-loop discipline, AGENTS.md form (read by DeepSeek Harness,
  OpenAI Codex, Cursor, Jules, Amp and other AGENTS.md-aware tools).
  Install: copy into your project root, or merge into an existing AGENTS.md.
  Monorepos: nested per-directory AGENTS.md wins closest-first; Codex users
  can also install globally at ~/.codex/AGENTS.md.
  Regenerated from adapters/_core.md - edit there, not here. {URL}
-->
# Research discipline for this project

{CORE}""",
    "gemini/GEMINI.md": f"""<!--
  breakthrough-loop discipline for Gemini CLI (project context file).
  Install: copy into your project root as GEMINI.md, or merge into yours.
  Regenerated from adapters/_core.md - edit there, not here. {URL}
-->
# Research discipline for this project

{CORE}""",
    "cline/breakthrough-loop.md": f"""<!--
  breakthrough-loop discipline for Cline.
  Install: mkdir -p .clinerules && cp this file into .clinerules/
  Regenerated from adapters/_core.md - edit there, not here. {URL}
-->
# Research discipline for this project

{CORE}""",
    "windsurf/breakthrough-loop.md": f"""---
trigger: always_on
---

<!-- breakthrough-loop discipline for Devin Desktop (formerly Windsurf). Install:
     mkdir -p .devin/rules && cp this file into .devin/rules/
     (.windsurf/rules/ is still read as a legacy path).
     Workspace rule files are capped at 12,000 characters - keep _core.md lean.
     Regenerated from adapters/_core.md - edit there, not here. {URL} -->
# Research discipline for this project

{CORE}""",
    "aider/CONVENTIONS.md": f"""<!--
  breakthrough-loop discipline for Aider.
  Install: save as CONVENTIONS.md, launch `aider --read CONVENTIONS.md`
  (or list it under `read:` in .aider.conf.yml).
  Regenerated from adapters/_core.md - edit there, not here. {URL}
-->
# Research discipline for this project

{CORE}""",
}


SKILL_SRC = HERE / "claude-code" / "breakthrough-loop" / "SKILL.md"
DSH_SKILL = HERE.parent / ".agents" / "skills" / "breakthrough-loop" / "SKILL.md"


def main() -> int:
    check = "--check" in sys.argv
    drift = []
    for rel, content in TARGETS.items():
        path = HERE / rel
        path.parent.mkdir(exist_ok=True)
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(rel)
        else:
            path.write_text(content, encoding="utf-8")
            print("wrote", path.relative_to(HERE.parent))
    skill = SKILL_SRC.read_text(encoding="utf-8")
    if check:
        if not DSH_SKILL.exists() or DSH_SKILL.read_text(encoding="utf-8") != skill:
            drift.append(".agents/skills/breakthrough-loop/SKILL.md")
    else:
        DSH_SKILL.parent.mkdir(parents=True, exist_ok=True)
        DSH_SKILL.write_text(skill, encoding="utf-8")
        print("wrote", DSH_SKILL.relative_to(HERE.parent))
    if drift:
        print("DRIFT (run python adapters/build.py):", ", ".join(drift))
        return 1
    if check:
        print("adapters match _core.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
