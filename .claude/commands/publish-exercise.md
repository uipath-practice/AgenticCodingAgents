Publish a draft exercise to the site navigation — makes it visible from the home screen and the navigation menu.

Exercises created with `/new-exercise` are accessible via direct URL but hidden from the navigation. Run this skill when the exercise content is ready for learners.

**Before proceeding, read:** `Master/Filesystem.md` (nav registration rules), `Master/CourseStructure.md` (overview page structure — used to derive nav labels and the home page card), and `Master/Localization.md` (nav label translations and the publish-time translation pass).

## Collect inputs

If the exercise slug is not provided, ask for it:

1. **Exercise slug** — folder name of the exercise (e.g., `expense-report-processing`)

---

## Step 1: Validate the exercise

1. Confirm `docs/<exercise-slug>/` exists on disk. If not, stop — nothing to publish.
2. Check whether the exercise already appears in `mkdocs.yml` nav. If it does, stop and inform the user — it's already published.

---

## Step 2: Discover pages

Scan `docs/<exercise-slug>/` and collect all pages in publication order:

1. `index.md` → nav label: `Overview`; read its `# Title` heading for the exercise display name
2. Lesson files (`N-verb-noun.md`) in ascending numeric order → read the `# Title` heading from each for its nav label, prefixed with the step number: `1. <Title>`, `2. <Title>`, etc.
3. `you-did-it.md` → nav label: `You did it!`

Build the nav block to be added:

```yaml
- <Exercise Display Name>:
  - Overview: <exercise-slug>/index.md
  - 1. <Lesson 1 Title>: <exercise-slug>/1-verb-noun.md
  - 2. <Lesson 2 Title>: <exercise-slug>/2-verb-noun.md
  - You did it!: <exercise-slug>/you-did-it.md
```

---

## Step 3: Check for an existing home page card

Read `docs/index.md`. Check whether a card or link for this exercise already exists (search for the exercise slug and display name). If not, prepare to add one using the format of existing exercise cards on the home page.

---

## Step 4: Show what will be added

Output a clear summary before making changes:

```
PUBLISHING: <exercise-slug>

Adding to mkdocs.yml nav (before "Next Steps"):
<full nav block, indented>

Adding to docs/index.md:
  <exercise card text, or "Already present">
```

Then proceed — no confirmation required for publishing.

---

## Step 5: Update mkdocs.yml

Insert the exercise nav block immediately before `- Next Steps: next-steps.md`.

---

## Step 5.5: Update mkdocs.local.yml

If `mkdocs.local.yml` exists, search it for a nav section whose title contains the exercise slug and ends with `[Unpublished]` (e.g., `- Conversational Agents [Unpublished]:`). Remove the entire section — the title line and all its child entries. If no matching entry is found, skip this step.

---

## Step 6: Update docs/index.md

If no home page card exists for this exercise, add one. Match the style of existing exercise entries (numbered description with a direct link).

---

## Step 6.5: Localize

1. In `mkdocs.yml`, add the exercise's new nav labels (display name and every lesson label) to the `nav_translations` block of **each** language under the `i18n` plugin. Use the glossary and tone rules in `Master/Localization.md`.
2. Run `/sync-translations <exercise-slug>` to create the translated pages. Include `docs/index.md` in the sync — the new home page card made its translations stale.

---

## Step 7: Verify

Run `mkdocs build`:

```bash
python3 -m mkdocs build
```

Report any errors. If the build passes, confirm what was done:
- Nav section added to `mkdocs.yml`
- Home page card added to `docs/index.md` (or was already present)
- Nav labels translated and page translations synced
- Build passed

Then show the live URL (once deployed):
> **URL tokens.** `<base-path>` is the path component of `site_url` in `mkdocs.yml`
> (e.g. `/MyCourse`); `<site-url>` is the full `site_url` value including its trailing
> slash. Read both from `mkdocs.yml` at run time — never hardcode a course or repo name.

```
<site-url><exercise-slug>/
```

And the local preview URL (if `mkdocs serve` is running):
```
http://127.0.0.1:8000<base-path>/<exercise-slug>/
```

$ARGUMENTS
