# HOWTO — Course Authoring Workflows

Step-by-step guides for every course authoring task. Covers both the assisted (Claude Code) and manual approaches.

---

## Workflow 1: Create a new exercise from scratch

### What you need before starting

- **Exercise name** — display name (e.g., "Expense Report Processing")
- **One-paragraph description** — what the learner will build and which platform features they'll use
- **List of lessons** — names with brief descriptions (e.g., "1. Upload Report — robot retrieves PDFs from a storage bucket")

### Using Claude Code

```
/new-exercise
Name: Expense Report Processing
Slug: expense-report-processing
Description: Automate expense report review using IXP extraction and human validation in Action Center.
Steps: 1. Upload Report — robot retrieves PDFs, 2. Extract Data — IXP reads fields, 3. Review Exceptions — Action Center task
```

The skill creates all folders, stub pages, and image folders. It does **not** add the exercise to the nav or the home page — the exercise starts as a draft, accessible only via direct URL. This prevents learners from seeing work-in-progress content.

At the end, the skill shows you the direct URLs for local preview:
> **URL tokens.** `<base-path>` is the path component of `site_url` in `mkdocs.yml`
> (e.g. `/MyCourse`); `<site-url>` is the full `site_url` value including its trailing
> slash. Read both from `mkdocs.yml` at run time — never hardcode a course or repo name.

- `http://127.0.0.1:8000<base-path>/<exercise-slug>/`

**To preview with full navigation:** add the exercise to `mkdocs.local.yml` using `[Unpublished]` in the title, then serve with `mkdocs serve -f mkdocs.local.yml`. This file is gitignored — it never affects the live site.

```yaml
  - Exercise Display Name [Unpublished]:
    - Overview: <exercise-slug>/index.md
    - 1. Lesson Title: <exercise-slug>/1-verb-noun.md
    - You did it!: <exercise-slug>/you-did-it.md
```

When the exercise is ready for learners, run `/publish-exercise`.

### Manual approach

1. Create the exercise folder: `docs/<exercise-slug>/`
2. Create image folders for each lesson: `docs/<exercise-slug>/<step-slug>.images/.gitkeep`
3. Create `documentation.txt` with the standard header (see [Filesystem.md](Filesystem.md))
4. Write `index.md` following the overview template in [CourseStructure.md](CourseStructure.md)
5. Write stub lesson files (`1-verb-noun.md`, `2-verb-noun.md`, etc.) following the lesson template
6. Write `you-did-it.md` following the summary template
7. Run `mkdocs build` to verify no errors — expected warning: "page not in navigation"
8. Register the exercise when ready: see Workflow 3 (Publish an exercise)

---

## Workflow 2: Generate a lesson from screenshots

This is the primary content generation workflow. You'll do this for each lesson after scaffolding the exercise.

### Prerequisites

- Exercise already scaffolded (Workflow 1 complete)
- Screenshots uploaded to the lesson's image folder: `docs/<exercise-slug>/<step-slug>.images/`
- Screenshots named in one of these formats:
  - **Sequential numeric:** `1.png`, `2.png`, `3.png`, etc., OR
  - **Mac screenshot format:** `Screenshot 2026-04-07 at 3.38.16 PM.png` (will be sorted by timestamp)
- `scripts/.env` configured with Azure OpenAI credentials
- Python dependencies installed: `pip install openai requests beautifulsoup4 numpy python-dotenv pillow`

### For new lessons (no .md file yet)

1. **Add documentation links** — Edit `docs/<exercise-slug>/documentation.txt` and add URLs to official UiPath docs relevant to this lesson's topic. The extraction script uses these as context.

2. **Run the lesson generation skill:**
   ```
   /new-lesson
   Exercise: expense-report-processing
   Step: 2
   Name: Extract Data
   Images: docs/expense-report-processing/extract-data.images/
   Context: IXP project reads line items from expense receipts. Outputs amount, category, date fields.
   ```

3. **What happens behind the scenes:**
   - Script fetches and embeds any new documentation URLs
   - Script analyzes each screenshot (in order) and writes `.metadata.json` files (one per image)
   - Script renames screenshots based on metadata content with sequential numbering: `1-configure-robot.png`, `2-add-trigger.png`, `3-verify-settings.png`, etc.
   - Claude reads the metadata and builds the complete lesson page
   - Screenshots are placed in context with step-by-step instructions

4. **Review the generated page** — Check that:
   - Screenshots are in the right order and context
   - Code blocks contain exactly what the learner should copy
   - Platform names are bold on first use
   - Technical accuracy matches what the screenshots actually show

5. **Edit and finalize** — Add details the screenshots don't capture:
   - Business context and explanations
   - Tips and warnings from your domain expertise
   - Cross-references to other lessons or exercises

### For adding steps to an existing lesson

If a lesson `.md` file already exists (stub or partial), the skill will:

1. **Extract metadata first** — Analyze all new screenshots in the folder without renaming them
2. **Rename based on content** — Use the extracted metadata (step_instruction and ui_description) to give each screenshot a meaningful name that describes what it shows (e.g., `select-agent-type.png`, `review-system-prompt.png` — not `1-step.png`)
3. **Generate descriptions** — Extract step instructions and UI descriptions from metadata
4. **Rename images** — Give each screenshot a sequential numeric prefix + descriptive name based on content
5. **Append to Steps section** — Add the new steps to the existing lesson's `## Steps` section while preserving the Goal and opening tip

To add steps to an existing lesson:

```
/new-lesson
Exercise: conversational-agents
Step: 1
Name: Creating a Conversational Agent
Images: docs/conversational-agents/1-create-agent.images/
```

The skill will:
- Detect the existing `1-create-agent.md` file
- Extract metadata from all images in the folder (whether named `1.png`, `2.png`... or `Screenshot 2026-04-07 at 3.38.16 PM.png`...)
- Rename them with sequential numbers + content-based slugs: `1-create-agent.png`, `2-select-type.png`, etc.
- Add the extracted steps to the lesson's `## Steps` section

---

**Direct URLs for local preview (after generation):**
- New lesson: `http://127.0.0.1:8000<base-path>/<exercise-slug>/N-verb-noun/`
- Updated lesson: same URL — the page has been updated in place

The lesson is part of a draft exercise — it's not visible in the nav until you run `/publish-exercise`.

---

## Workflow 3: Publish an exercise

Once all lessons are written, reviewed, and ready for learners, publish the exercise to make it visible.

```
/publish-exercise expense-report-processing
```

The skill:
1. Reads the exercise folder to discover all pages
2. Derives nav labels from each page's `# Title` heading
3. Adds the nav section to `mkdocs.yml`
4. Adds a home page card to `docs/index.md`
5. Runs `mkdocs build` to verify
6. Shows the live URL (once deployed to GitHub Pages)

### Manual approach

1. Add a nav section to `mkdocs.yml` before `- Next Steps: next-steps.md`:
   ```yaml
   - Exercise Display Name:
     - Overview: exercise-slug/index.md
     - 1. Lesson Title: exercise-slug/1-verb-noun.md
     - You did it!: exercise-slug/you-did-it.md
   ```
2. Add an exercise card to `docs/index.md` matching the format of existing entries
3. Run `mkdocs build` to verify

---

## Workflow 4: Review a lesson

After you've written and edited a lesson, run the review skill to check it against all formatting and language rules.

```
/review-lesson categorizing-incidents/1-llm-with-context
```

The skill reads the lesson page and checks it against:
- [CourseStructure.md](CourseStructure.md) — page structure rules
- [Formatting.md](Formatting.md) — all formatting patterns
- [Language.md](Language.md) — voice, tone, word choices

It reports issues organized by severity:
- **Must fix** — broken formatting, missing required sections, forbidden words
- **Recommend** — structure deviations, inconsistent patterns
- **Info** — minor style suggestions

Fix the must-fix items, consider the recommendations, and ignore the info items at your discretion.

---

## Workflow 5: Review an exercise

Once all lessons are reviewed individually, run the exercise-level review for cross-lesson coherence.

```
/review-exercise invoice-matching-ixp
```

This checks everything the lesson review checks, plus:
- Overview page links match actual lesson files
- Nav registration in `mkdocs.yml` is correct and complete (if published)
- Consistent terminology and platform name usage across all pages
- Step numbering is sequential with no gaps
- Summary page component table matches the actual exercise components
- All referenced images exist on disk
- No orphaned images (images that exist but aren't referenced)
- Cross-lesson links are valid

---

## Workflow 6: Remove a lesson

Use this to retire a single lesson while keeping the rest of the exercise intact.

```
/remove-lesson invoice-matching-ixp/2-configure-robot
```

The skill scans everything that will change — the lesson file, its image folder, its nav entry, and its step table row — and shows a full summary. **You must type `yes` to confirm before any changes are made.**

On confirmation:
- Lesson `.md` file and image folder are moved to `Archive/<exercise-slug>/`
- Nav entry is removed (if the exercise was published)
- Step table row is removed from the exercise overview page
- Remaining lesson labels are renumbered to close the gap
- Build is verified

Lesson filenames are not renamed — their URLs remain unchanged.

---

## Workflow 7: Remove an exercise

Use this to retire an entire exercise — for example, when retiring a topic or resetting after a test run.

```
/remove-exercise invoice-matching-ixp
```

The skill scans the entire exercise folder, its nav section, and home page references, then shows a full summary. **You must type `yes` to confirm before any changes are made.**

On confirmation:
- The entire `docs/<exercise-slug>/` folder is moved to `Archive/<exercise-slug>/`
- The nav section is removed from `mkdocs.yml` (if published)
- Home page references are removed from `docs/index.md`
- Build is verified

The `Archive/` folder is gitignored — archived content is never deployed.

---

## Workflow 8: Edit and refine existing content

When making changes to an existing page:

1. **Read the page first** — understand the current structure before changing anything
2. **Match existing patterns** — don't introduce new section types or formatting
3. **Preserve content** — rephrase awkward sentences, don't delete explanatory paragraphs
4. **Update all occurrences** — if you change a prompt in a code block, search for the same text elsewhere on the page
5. **Run `mkdocs build`** — verify no broken links after editing

### Common editing tasks

| Task | What to do |
|------|-----------|
| Fix language/tone | Apply rules from [Language.md](Language.md). Rephrase, don't delete. |
| Add screenshot | Place in the lesson's image folder, reference with `.screenshot` class |
| Update a prompt | Use the diff + highlighted code block pattern from [Formatting.md](Formatting.md) |
| Add a tip/warning | Use one of the four admonition types (tip, info, note, warning) |
| Restructure a page | Only with explicit confirmation — human structure choices are intentional |

---

## Workflow 9: Start a new course in a new repository

Reusing this toolchain for a different course. Do these in order — the gates at steps 8 and 9
exist to catch the expensive mistakes early.

### 1. Fill in the course profile FIRST

Edit `Master/CourseProfile.md`. Every later step reads from it. Decide `SITE_URL` carefully: it
produces the path prefix on every built link, the sitemap, and the dev-server URL, and a wrong
value builds fine locally while breaking every asset on the live site.

### 2. Clone the target repo — never re-point an existing clone's origin

```bash
git clone https://github.com/<ORG>/<REPO>.git
cd <REPO>
git config user.name  "<Your Name>"
git config user.email "<your@email>"
```

Repo-local identity is required if there is no global `~/.gitconfig` — commits hard-fail
otherwise. Prefer a working copy **outside** any cloud-sync folder (OneDrive, Dropbox, iCloud):
sync daemons contend with `.git/index.lock` and can materialise placeholder files mid-command.

If the repo's default branch is not `main`, either rename it or edit the `branches:` list in
`.github/workflows/deploy.yml` — the deploy only triggers on `main`.

### 3. Copy the toolchain

Copy verbatim: `Master/`, `.claude/commands/`, `scripts/` (excluding `.env`,
`context/vector_store.json`, `__pycache__`), `hooks/`, `.github/`, `.gitignore`,
`requirements.txt`, `docs/stylesheets/`, `docs/javascripts/`, `docs/assets/images/`.

Do **not** copy: any exercise folder, any `*.<locale>.md`, exercise-specific assets (PDFs,
`dependencies/`), `scripts/.env`, `mkdocs.local.yml`.

`hooks/split_cols.py` and the `.img-cols*` rules in `docs/stylesheets/extra.css` are two halves of
one feature — never separate them. Both also need `md_in_html` in `markdown_extensions`.

### 4. Run the de-hardcoding checklist

Run every grep in `Master/CourseProfile.md` → "Propagation checklist". In particular: no absolute
paths to a mkdocs binary (use `python3 -m mkdocs`, which works regardless of how mkdocs was
installed and does not depend on PATH), and no previous course's repo name, site URL, or tenant.

### 5. Rewrite `mkdocs.yml`

Set `site_name`, `site_url`, `site_description`, `site_author`. Reduce `nav:` to `Home` +
`Next Steps`. **`- Next Steps: next-steps.md` must remain the literal last nav entry** —
`/publish-exercise` inserts each exercise block immediately before it, and
`scripts/translation_status.py` scrapes this block to tell published pages from drafts.

If the logo or favicon filenames change, update `theme.logo` / `theme.favicon` too, or `--strict`
fails on the missing file.

### 6. Decide the locale set — four files, one atomic change

`mkdocs.yml` (`i18n` locales) · `requirements.txt` (`mkdocs-static-i18n`, plus `jieba` only for
`zh`) · `scripts/translation_status.py` (`LANGUAGES`) · each locale's `nav_translations` map. These
must agree. A plugin block with the dependency removed fails the build with
`The "i18n" plugin is not installed`. See `Master/Localization.md` → "Adding a locale later".

### 7. Create the fresh content pages

`docs/index.md` (home) and `docs/next-steps.md` (global outro). Also create `mkdocs.local.yml` by
hand — it is a **standalone config, not an overlay**, so `cp mkdocs.yml mkdocs.local.yml`. It is
gitignored, so it never arrives with a clone and must be recreated on each machine;
`/new-exercise` expects to be able to append draft entries to it.

Do not link to a page that does not exist yet: `validation.links.not_found` defaults to `warn`,
which `--strict` promotes to an error. Create lesson stubs before linking them from an overview.

### 8. Gate: build and serve locally

```bash
python3 -m mkdocs build --strict     # must exit 0
python3 scripts/translation_status.py # must exit 0
python3 -m mkdocs serve               # must serve at http://127.0.0.1:8000<BASE_PATH>/
```

If the dev server 404s at that path, `site_url` is wrong. This is the cheapest possible check on
the one value that breaks the live deploy. Note that pages absent from `nav:` log at INFO, not
warning — drafts do **not** fail `--strict`.

### 9. Gate: prove the deploy chain while the site is still almost empty

On GitHub, before the first push: **Settings → Actions → General → Workflow permissions** = "Read
and write" (otherwise `gh-deploy`'s push to `gh-pages` 403s). Set up push auth — with no `gh` CLI
and no SSH key, `git config credential.helper osxkeychain` plus a fine-grained PAT scoped to the
repo with `Contents: read and write` is the least machinery. Run the first `git push` from a real
terminal so the credential prompt works; never put the PAT in the remote URL. If the org enforces
SAML SSO, authorize the token for the org.

Push, watch the Action, then **Settings → Pages → Source** = branch `gh-pages`, folder `/ (root)`
(the branch only exists after the first successful run). Confirm the live URL loads.

Debugging a `site_url` 404 is trivial now and miserable after the course is written.

### 10. Author the content

Per exercise: `/new-exercise` → add screenshots to `docs/<slug>/<lesson-slug>.images/` → seed
`docs/<slug>/documentation.txt` → `/new-lesson` per lesson → `/review-lesson` → `/review-exercise`
→ `/publish-exercise <slug>` → push.

**Migrating a course that already has written content?** Put the existing prose in
`source/<exercise-slug>/<N-lesson-slug>.md`. `/new-lesson` Step 0 treats it as authoritative and
reshapes it into the template instead of rewriting it. Name harvested screenshots
`N-descriptive-name[-W].png` up front so Step 2.5's rename can be skipped.

## Workflow 10: Sync translations

English is the master language — translations are derived, never edited by hand. Full rules: `Localization.md`.

1. Edit English content as usual.
2. Check what's out of date:

   ```bash
   python3 scripts/translation_status.py
   ```

3. Run `/sync-translations` (optionally scoped to an exercise, page, or language). It translates missing pages, re-translates stale ones, and updates source hashes.
4. Review the diff, then `mkdocs build` and commit.

New drafts are not translated until published — `/publish-exercise` includes the translation pass.

---

## Best practices for course design

### Planning an exercise

- **Start with the business case.** What real-world problem does the learner solve? Lead with that.
- **Identify 3–6 lessons.** Each lesson should take 15–30 minutes. If a lesson would take longer, split it.
- **Each lesson produces a visible result.** The learner should be able to test or see something working at the end of every lesson.
- **Progressive complexity.** Start with the simplest component and build toward the full solution.

### Writing lessons

- **Background before steps.** Don't assume the learner knows why they're doing something — explain briefly, then show how.
- **One screenshot per action.** Don't show 5 screenshots for a single click. Show the result that confirms they did it right.
- **Test every prompt and code block.** Copy-paste your own code blocks and verify they work exactly as written.
- **End with validation.** Every lesson should end with the learner confirming something works — a debug run, a test output, a visible result.

### Reviewing content

- **Read aloud.** If a sentence sounds awkward when spoken, rewrite it.
- **Check the learner's path.** Follow the steps as if you've never seen the platform. Would you know where to click?
- **Verify screenshots match instructions.** If the UI has changed since the screenshot was taken, update both.
- **Test cross-references.** Click every internal link. Run `mkdocs build` to catch broken ones automatically.
