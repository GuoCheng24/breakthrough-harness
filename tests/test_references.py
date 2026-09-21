"""The reference list is held to the same standard as everything else on the page.

"Where the skeleton comes from" once cited FunSearch as Nature 2023. The paper went
online in December 2023 and is Nature 625, 468-475 (2024); anyone who looked it up
found the page wrong on the one line that was supposed to be checkable. None of the
five entries carried an identifier, so nothing could have caught it.

Two layers, because network is not something a push should depend on:

  always     every entry carries a resolvable identifier (DOI, arXiv id, or URL), and
             the year it states is the year the identifier resolves to -- recorded
             here, next to the identifier, so a wrong year is a diff and not a memory.
  scheduled  with REFERENCES_ONLINE=1 the DOIs are resolved at Crossref and the arXiv
             id at export.arxiv.org, and the recorded year and first author are
             compared with what comes back. CI runs this weekly.
"""
import json
import os
import re
import urllib.request

import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]

# identifier -> (year the page must state, family name of the first author)
EXPECTED = {
    "10.1038/s41586-023-06924-6": (2024, "Romera-Paredes"),
    "10.1126/science.aaa9375": (2015, "Dwork"),
    "2502.18864": (2025, "Gottweis"),
    "proceedings.mlr.press/v97/recht19a.html": (2019, "Recht"),
    "github.com/google-research/tuning_playbook": (2023, "Godbole"),
}

IDENT = re.compile(r"10\.\d{4,}/[^\s)\]]+|arXiv:(\d{4}\.\d{4,5})|https?://(\S+?)[)\s]")


def _reference_bullets(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    m = re.search(r"^## (Where the skeleton comes from|骨架的出处).*?(?=^## |\Z)", text,
                  re.S | re.M)
    assert m, f"{path}: the references section is missing"
    bullets = re.split(r"^- ", m.group(0), flags=re.M)[1:]
    assert len(bullets) == len(EXPECTED), f"{path}: {len(bullets)} entries, expected {len(EXPECTED)}"
    return [" ".join(b.split()) for b in bullets]


def _identifier(bullet):
    for key in EXPECTED:
        if key in bullet:
            return key
    return None


@pytest.mark.parametrize("path", ["README.md", "README.zh-CN.md"])
def test_every_reference_carries_an_identifier_and_the_right_year(path):
    seen = set()
    for b in _reference_bullets(path):
        key = _identifier(b)
        assert key, f"{path}: no known identifier in: {b[:80]}"
        assert key not in seen, f"{path}: {key} cited twice"
        seen.add(key)
        year, author = EXPECTED[key]
        assert str(year) in b, f"{path}: {key} must state {year}: {b[:100]}"
        # the one year that was wrong must not come back
        assert not re.search(r"Nature 2023", b), f"{path}: FunSearch is Nature 2024, not 2023"
        assert author in b or path.endswith("zh-CN.md") and key.startswith("github.com"), \
            f"{path}: {key} does not name {author}"
    assert seen == set(EXPECTED), f"{path}: missing {set(EXPECTED) - seen}"


def _get(url, accept=None):
    req = urllib.request.Request(url, headers={"User-Agent": "breakthrough-harness reference check",
                                               **({"Accept": accept} if accept else {})})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


@pytest.mark.skipif(not os.environ.get("REFERENCES_ONLINE"),
                    reason="resolves identifiers over the network; set REFERENCES_ONLINE=1")
def test_identifiers_resolve_to_the_recorded_year_and_author():
    for key, (year, author) in EXPECTED.items():
        if key.startswith("10."):
            m = json.loads(_get(f"https://api.crossref.org/works/{key}", "application/json"))["message"]
            got_year = (m.get("published-print") or m.get("issued"))["date-parts"][0][0]
            got_author = m["author"][0]["family"]
        elif re.fullmatch(r"\d{4}\.\d{4,5}", key):
            xml = _get(f"https://export.arxiv.org/api/query?id_list={key}")
            got_year = int(re.search(r"<published>(\d{4})", xml).group(1))
            got_author = re.search(r"<name>[^<]*?(\S+)</name>", xml).group(1)
        else:
            html = _get(f"https://{key}")
            got_year, got_author = year, author          # a web page: reachability is the check
            assert author.split("-")[0].lower() in html.lower() or "tuning" in html.lower(), key
        assert got_year == year, f"{key}: page says {year}, source says {got_year}"
        assert got_author.lower() in author.lower() or author.lower() in got_author.lower(), \
            f"{key}: page names {author}, source names {got_author}"
