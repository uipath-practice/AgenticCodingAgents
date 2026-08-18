# Course Profile

**Single source of truth for every course-specific value in this repo.** When reusing this
toolchain for a new course, fill in this table first, then run the propagation checklist at the
bottom. Never invent a tenant URL, contact address, or site URL — read it from here.

| Key | Value |
|---|---|
| `COURSE_TITLE` | Agentic Coding Agents |
| `COURSE_DESCRIPTION` | TODO_ONE_LINE_DESCRIPTION |
| `SITE_AUTHOR` | Mihai Iorga |
| `SITE_URL` | `https://uipath-practice.github.io/AgenticCodingAgents/` |
| `BASE_PATH` | `/AgenticCodingAgents` |
| `REPO_URL` | `https://github.com/uipath-practice/AgenticCodingAgents` |
| `DEFAULT_BRANCH` | `main` |
| `TRAINING_PLATFORM_URL` | `https://cloud.uipath.com/tpenlabs` |
| `TRAINING_TENANT` | `AgenticWorkshop` |
| `CONTACT_EMAIL` | mihai.iorga@uipath.com |
| `LOCALES` | `en` (English only) |
| `MKDOCS_CMD` | `python3 -m mkdocs` |
| `PLATFORM_NAMES` | Studio Web, Studio, Orchestrator, Maestro, Action Center, Integration Service, Data Fabric, Context Grounding, IXP, Agent Builder, Autopilot, AI Trust Layer, Storage Buckets |

`BASE_PATH` and `SITE_URL` must agree with each other and with `site_url` in `mkdocs.yml`.
`SITE_URL` is the single most consequential value in the repo: it produces the path prefix on
every built link, the sitemap, and the dev-server URL. A wrong value builds fine locally and
breaks every asset on the live site.

If the course has no shared training environment, set `TRAINING_PLATFORM_URL` and
`TRAINING_TENANT` to `NONE` and **remove** the "Training Environment" callout from
`Master/CourseStructure.md` and `Master/Templates/index.md` rather than leaving a wrong URL.

## Propagation checklist

Run each grep; every hit must be either updated to this table's values or deliberately left:

```bash
# 1. No previous course's URL, repo, or tenant survives anywhere.
#    Update this pattern per course: it must list the PREVIOUS course's values, never this one's.
#    (`tpenlabs` and `uipath-practice` are THIS course's correct values -- do not add them here.)
grep -rn 'AgenticPracticeCourse\|AgenticPractice\b' . --exclude-dir=.git --exclude-dir=Archive

# 2. No absolute machine paths (the mkdocs binary was hardcoded in the original)
grep -rn '/Users/' . --exclude-dir=.git --exclude-dir=site

# 3. No unfilled placeholders
grep -rn 'TODO_' . --exclude-dir=.git

# 4. Locale config agrees in all three places
grep -n 'locale:' mkdocs.yml
grep -n '^LANGUAGES' scripts/translation_status.py
grep -n 'i18n' requirements.txt

# 5. Training-environment callout: these are the template locations that seed every page
grep -rn 'Training Environment' Master/

# 6. Contact address
grep -rn 'CONTACT_EMAIL\|@' docs/next-steps.md
```

Then the build gates:

```bash
python3 -m mkdocs build --strict     # must exit 0
python3 scripts/translation_status.py # must exit 0
python3 -m mkdocs serve               # must serve at http://127.0.0.1:8000<BASE_PATH>/
```
