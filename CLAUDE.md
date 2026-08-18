# CLAUDE.md — Agentic Coding Agents

This file is read automatically on every Claude Code session in this project.
Apply all rules below to every task involving this site — no reminders needed.

---

## Course Profile — read this before inventing any value

`Master/CourseProfile.md` is the single source of truth for every course-specific value: site URL,
base path, repo, training environment, contact address, product names. **Never invent a tenant
URL, a contact address, or a site URL — read it from there.** When a value appears wrong or
missing, fix `CourseProfile.md` and propagate, rather than hardcoding it at the call site.

**Live site:** https://uipath-practice.github.io/AgenticCodingAgents/
**Source repo:** https://github.com/uipath-practice/AgenticCodingAgents
**Theme:** MkDocs Material (`mkdocs.yml`)
**Deploy:** GitHub Actions on every push to `main` (`.github/workflows/deploy.yml`)

> **URL tokens** used throughout the command files: `<base-path>` is the path component of
> `site_url` in `mkdocs.yml`; `<site-url>` is the full `site_url` including its trailing slash.
> Read them from `mkdocs.yml` at run time.

---

## Master Reference Files

All detailed rules, templates, and formatting conventions live in `Master/`. Read the relevant file
before creating or reviewing content:

| File | What it covers |
|------|---------------|
| `Master/CourseProfile.md` | Every course-specific value + the reuse propagation checklist |
| `Master/README.md` | Entry point — what each file contains, sanity rules |
| `Master/Filesystem.md` | Directory structure, file/folder naming, image conventions |
| `Master/CourseStructure.md` | Page types (Overview, Lesson, Summary) with full templates |
| `Master/Formatting.md` | Images, two-column layouts, code blocks, admonitions, tables, prompt diffs, argument docs |
| `Master/Language.md` | Voice, tone, humour, word choices, platform names |
| `Master/Localization.md` | Locale set and the translation sync workflow (English-only today) |
| `Master/HOWTO.md` | End-to-end workflows: create exercise, generate lesson, publish, remove, review, validate |

**When creating new content:** read `Master/CourseStructure.md` and `Master/Formatting.md` first.
**When reviewing content:** use `/review-lesson` and `/review-exercise`.
**When editing language:** read `Master/Language.md`.

---

## Quick Reference (always in context)

### Language essentials
- **Second person, direct:** "you'll configure", "your agent", "open the panel"
- **Short sentences.** One idea per sentence. Paragraphs: 2–4 sentences max.
- **Conversational and warm** — not corporate, not sloppy. Humour welcome where natural.
- **Avoid:** "leverage", "utilize", "robust", "seamlessly", "In this section we will", "Please note that", "It is important to", "feel free to"
- **Platform names:** Bold on first appearance per page. Exact names for this course are listed as
  `PLATFORM_NAMES` in `Master/CourseProfile.md` — use that list, not a remembered one.

### Formatting essentials
- **Code blocks:** Every copyable string in a fenced code block with a language identifier. Never bare ` ``` `.
- **Screenshots:** `{ .screenshot }` for all UI screenshots. Wide images (`-W`) use `width="900"`.
- **Two-column:** `[[[...|N|...]]]` shorthand (processed by `hooks/split_cols.py`, styled by the
  `.img-cols*` rules in `docs/stylesheets/extra.css` — the two are one feature, never separate them).
- **Admonitions:** Only `tip`, `info`, `note`, `warning`.
- **No bottom nav links.** The MkDocs sidebar handles navigation.
- Screenshot metadata carries a `layout.mode` (`full_width` / `split_50` / `split_30`) — that is the
  pre-computed layout decision. Use it rather than judging image width by eye.

### Localization essentials
- **This course is English-only.** The `i18n` plugin is configured with a single `en` locale and
  `LANGUAGES` in `scripts/translation_status.py` is `[]`, so `/sync-translations` is a no-op.
- To add a language, see `Master/Localization.md` → "Adding a locale later". Four files must change
  together; nothing you author now makes it harder.

### File naming
- Exercise folder: lowercase, hyphenated
- Overview: always `index.md` (its H1 is read as the exercise name by the metadata pipeline)
- Lessons: `N-verb-noun.md`, sequential with no gaps
- Images: per-lesson folder `<lesson-slug>.images/`, matching the lesson filename **including its
  numeric prefix**
- Summary: `you-did-it.md` (no prefix)

---

## Behavioural Rules

### When editing an existing page
- Match existing structure. Don't introduce new section patterns.
- **Never remove sections, paragraphs, or explanatory text.** Rephrase — don't delete.
- If editing a prompt in a code block, update all occurrences on the page.
- **Capitalised domain concepts are intentional.** Don't lowercase them.

### When the course has existing source prose
- If `source/<exercise-slug>/<N-lesson-slug>.md` exists, **it is authoritative.** Reshape it into
  the template; do not paraphrase, condense, or rewrite the author's wording.
- Never invent steps, UI labels, or values absent from the source and from the screenshots.
- `extraction.ocr_text` in a screenshot's metadata is the ground truth for any string the learner
  must type.

### When creating new content
- Follow the templates in `Master/CourseStructure.md` exactly.
- New exercises and lessons start as **drafts** — do NOT add them to `nav:` in `mkdocs.yml` or to
  `docs/index.md`. Use `/publish-exercise` to promote when ready.
- When removing pages, use `/remove-lesson` or `/remove-exercise`: they move files to `Archive/`.
  Never delete.
- Run `python3 -m mkdocs build --strict` before committing. Pages absent from `nav:` log at INFO and
  do **not** fail `--strict`; a link to a page that doesn't exist yet **does**.

### When reviewing content
- If the human changed structure from the template, flag it but don't rewrite without confirmation.
- Don't add stub placeholders to sections the author intentionally left as future work.

---

## mkdocs.yml — Do Not Change Without Reason

- Theme `material`; the palette and feature list are deliberate
- `markdown_extensions`: all currently listed are in use. `attr_list` and `md_in_html` are
  load-bearing for `{ .screenshot }` and the two-column hook — removing either breaks pages silently
- `- Next Steps: next-steps.md` must remain the **last** `nav:` entry: `/publish-exercise` inserts
  each exercise block immediately before it, and `scripts/translation_status.py` scrapes `nav:` to
  tell published pages from drafts
- `site_url` must match the GitHub Pages URL exactly, trailing slash included

---

## Local Preview

```bash
python3 -m mkdocs serve
```

Serves at `http://127.0.0.1:8000<base-path>/` — the subpath comes from `site_url`, so a bare
`http://127.0.0.1:8000/` redirects. To preview drafts with full navigation:

```bash
python3 -m mkdocs serve -f mkdocs.local.yml
```

Build check before committing:
```bash
python3 -m mkdocs build --strict
```
