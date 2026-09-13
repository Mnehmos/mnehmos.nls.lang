"""Docs-site integrity: nav paths, internal links, and anchors.

The MkDocs site deploys on every push to master (`docs.yml`), so a broken
nav entry or dead link would only surface after merge.  These checks run
in the normal test suite instead.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
MKDOCS = REPO_ROOT / "mkdocs.yml"


def _nav_entries() -> list[str]:
    text = MKDOCS.read_text(encoding="utf-8")
    return re.findall(r":\s*([A-Za-z0-9_./-]+\.md)\s*$", text, re.MULTILINE)


def _slugify(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def _anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            anchors.add(_slugify(match.group(2)))
    return anchors


def test_every_nav_entry_exists():
    missing = [
        entry for entry in _nav_entries() if not (DOCS / entry).exists()
    ]
    assert missing == []


def test_every_doc_page_is_in_the_nav():
    nav = set(_nav_entries())
    pages = {
        str(path.relative_to(DOCS)).replace("\\", "/")
        for path in DOCS.rglob("*.md")
    }
    # Stylesheets and assets are not pages; every .md must be reachable.
    assert pages - nav == set()


def test_internal_links_resolve():
    broken: list[str] = []
    pattern = re.compile(r"\]\(([^)\s]+\.md)(#[^)\s]*)?\)")
    for page in DOCS.rglob("*.md"):
        text = page.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://")):
                continue
            if not (page.parent / target).exists() and not (DOCS / target).exists():
                broken.append(f"{page.name}: {target}")
    assert broken == []


def test_internal_anchors_resolve():
    broken: list[str] = []
    pattern = re.compile(r"\]\(([^)\s]+\.md)#([^)\s]+)\)")
    for page in DOCS.rglob("*.md"):
        text = page.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target, anchor = match.group(1), match.group(2)
            if target.startswith(("http://", "https://")):
                continue
            candidate = page.parent / target
            if not candidate.exists():
                candidate = DOCS / target
            if not candidate.exists():
                continue  # reported by test_internal_links_resolve
            if anchor not in _anchors(candidate):
                broken.append(f"{page.name}: {target}#{anchor}")
    assert broken == []


def test_landing_page_does_not_advertise_stale_counts():
    """The landing page's test count must match the suite's actual size."""
    import subprocess
    import sys

    index = (DOCS / "index.md").read_text(encoding="utf-8")
    match = re.search(r"\*\*([\d,]+) tests passing\*\*", index)
    if match is None:
        # A count in a table cell is fine too; only a stated number matters.
        return
    advertised = int(match.group(1).replace(",", ""))
    collected = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--collect-only"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    count_match = re.search(r"(\d+) tests? collected", collected.stdout)
    assert count_match is not None, collected.stdout[-500:]
    actual = int(count_match.group(1))
    assert advertised == actual, (
        f"docs/index.md advertises {advertised} tests but the suite has {actual}; "
        "update the landing page when the count changes."
    )
