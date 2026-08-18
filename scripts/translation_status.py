#!/usr/bin/env python3
"""
Translation status report — English is the master language.

Compares every English page in docs/ against its translations
(<page>.<locale>.md siblings) using the source_hash recorded in each
translation's front-matter.

Statuses:
    current  — translation exists and its source_hash matches the English file
    stale    — translation exists but the English file changed since translation
    missing  — published English page with no translation
    draft    — English page not registered in mkdocs.yml nav (informational;
               drafts are translated at publish time)

Usage:
    python3 scripts/translation_status.py            # full report
    python3 scripts/translation_status.py --quiet    # summary + problems only
    python3 scripts/translation_status.py --strict   # exit 1 if stale/missing
    python3 scripts/translation_status.py --hash docs/index.md   # print hash

Stdlib only. Portable: copy this file to any repository using the same
framework and adjust LANGUAGES if its language set differs
(see Master/Localization.md).
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- config ---
LANGUAGES = []  # translated locales (never includes English).
# English-only course: empty. When you add an i18n locale to mkdocs.yml, add its
# code here too -- the two must stay in sync. See Master/Localization.md.
DOCS_DIR = "docs"
MKDOCS_YML = "mkdocs.yml"
# ----------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
SUFFIX_RE = re.compile(r"\.(" + "|".join(LANGUAGES) + r")\.md$")
NAV_PATH_RE = re.compile(r"^\s*-?\s*[^#:]*:\s*(\S+\.md)\s*$")
HASH_RE = re.compile(r"^source_hash:\s*([0-9a-f]+)\s*$", re.MULTILINE)


def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def nav_pages() -> set:
    """Extract .md paths referenced in the nav section of mkdocs.yml."""
    pages, in_nav = set(), False
    for line in (ROOT / MKDOCS_YML).read_text(encoding="utf-8").splitlines():
        if re.match(r"^nav\s*:", line):
            in_nav = True
            continue
        if in_nav:
            if line.strip() and not line.startswith((" ", "\t", "-")):
                break  # left the nav block (new top-level key)
            m = NAV_PATH_RE.match(line)
            if m:
                pages.add(m.group(1))
    return pages


def english_pages():
    """All English .md files under docs/, relative to docs/."""
    docs = ROOT / DOCS_DIR
    for p in sorted(docs.rglob("*.md")):
        rel = p.relative_to(docs).as_posix()
        if not SUFFIX_RE.search(rel):
            yield rel, p


def translation_hash(path: Path):
    """source_hash from a translation's front-matter, or None."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    m = HASH_RE.search(text[:end if end != -1 else 400])
    return m.group(1) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--quiet", action="store_true", help="summary + problems only")
    ap.add_argument("--strict", action="store_true", help="exit 1 if stale/missing")
    ap.add_argument("--hash", metavar="FILE", help="print source hash of FILE and exit")
    args = ap.parse_args()

    if args.hash:
        print(file_hash(ROOT / args.hash))
        return 0

    published = nav_pages()
    counts = {"current": 0, "stale": 0, "missing": 0, "draft": 0}
    rows = []

    for rel, path in english_pages():
        is_draft = rel not in published
        src_hash = file_hash(path)
        for lang in LANGUAGES:
            t_path = path.with_name(path.name[:-3] + f".{lang}.md")
            if not t_path.exists():
                status = "draft" if is_draft else "missing"
            elif translation_hash(t_path) == src_hash:
                status = "current"
            else:
                status = "stale"
            counts[status] += 1
            rows.append((status, lang, rel))

    label = {"current": "  OK   ", "stale": " STALE ", "missing": "MISSING", "draft": " draft "}
    for status, lang, rel in rows:
        if args.quiet and status in ("current", "draft"):
            continue
        print(f"[{label[status]}] {lang}  {rel}")

    total = sum(counts.values())
    print(f"\n{total} checks: {counts['current']} current, {counts['stale']} stale, "
          f"{counts['missing']} missing, {counts['draft']} draft (not in nav — skipped)")
    if counts["stale"] or counts["missing"]:
        print("Run /sync-translations to update. See Master/Localization.md.")
        if args.strict:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
