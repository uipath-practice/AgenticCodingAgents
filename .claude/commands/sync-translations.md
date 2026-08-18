Synchronize translations with the English master content — translates missing pages, re-translates stale ones, and updates source hashes.

English is the master language. This skill propagates English changes to all translated languages. It never modifies English files.

**Before proceeding, read:** `Master/Localization.md` (translation rules, glossary, tone per language — non-negotiable) and `Master/Language.md` (the English voice the translations should carry).

## Collect inputs

Optional scope argument. If none is given, sync everything.

1. **Scope** (optional) — an exercise slug (`invoice-matching-ixp`), a single page path (`docs/index.md`), or a language (`zh` / `ko`)

---

## Step 1: Get the status

```bash
python3 scripts/translation_status.py
```

Collect all pages reported **stale** or **missing**, filtered by scope if one was given. Ignore **draft** pages — drafts are translated at publish time by `/publish-exercise`.

If nothing is stale or missing, report that and stop.

---

## Step 2: Show the work plan

```
SYNC TRANSLATIONS
────────────────────────────────────────────
To translate (missing):
  zh  docs/<page>.md → docs/<page>.zh.md
  ...
To re-translate (stale):
  ko  docs/<page>.ko.md  (English changed since translation)
  ...
```

Then proceed — no confirmation required.

---

## Step 3: Translate each page

For every page in the plan, per language:

1. Read the current English source in full.
2. Get its hash: `python3 scripts/translation_status.py --hash docs/<page>.md`
3. Write the translation to `docs/<page>.<locale>.md` (same folder, same name, locale suffix), starting with:

    ```yaml
    ---
    source_hash: <hash from step 2>
    ---
    ```

4. Apply `Master/Localization.md` strictly. The short version:
    - Translate prose, headings, admonition titles and content, table content, link text, alt text
    - **Keep English:** everything the learner types or pastes (all fenced code block contents), UI labels, platform names, capitalised domain concepts, URLs, paths, link targets
    - **Preserve verbatim:** code fences with language identifiers, `[[[ |N| ]]]` column markers, `{ .screenshot }` and other attribute lists, admonition type keywords (`tip`, `info`, `note`, `warning`)
    - Use the glossary terms consistently; follow the per-language tone rules
5. For **stale** pages: re-translate from the current English source. Use the existing translation as reference for consistent terminology, but the English source wins on structure and content.

Translation is structural mirroring: same headings, same paragraph breaks, same admonitions, same tables, same images in the same places. If the English page has 12 blocks, the translation has 12 blocks.

---

## Step 4: Verify

1. Re-run the status — everything in scope must now be **current**:

    ```bash
    python3 scripts/translation_status.py --quiet
    ```

2. Build the site:

    ```bash
    python3 -m mkdocs build
    ```

3. Spot-check one translated file: front-matter present, code blocks byte-identical to English, column markers and `{ .screenshot }` intact.

Report: pages translated per language, pages re-translated, and the resulting status summary.

$ARGUMENTS
