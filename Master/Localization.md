# Localization

How localized versions of the public course content work: file conventions, translation rules, and the sync workflow. Only learner-facing pages are localized — Master files, CLAUDE.md, skills, and scripts stay English.

---

## Languages

> **This course is currently English-only.** The localization machinery below is installed and
> dormant: the `i18n` plugin is configured in `mkdocs.yml` with a single `en` locale, and
> `LANGUAGES` in `scripts/translation_status.py` is `[]`. `/sync-translations` is a no-op until a
> locale is added. Nothing you author now makes adding a language later harder — suffix mode puts
> `page.<locale>.md` beside `page.md`, so no files move and no content is restructured.

| Locale | Name | URL prefix | Role |
|--------|------|-----------|------|
| `en` | English | `/` (site root) | **Master language.** All authoring happens here. |

Rows for translated locales go here as they are added. Example shape, from the course this
toolchain came from: `zh` → 简体中文 at `/zh/`, `ko` → 한국어 at `/ko/`.

English is always the source of truth. Translations are derived from it and never edited independently — fixes go into the English page first, then propagate.

---

## How it's built

The site uses the `mkdocs-static-i18n` plugin (suffix mode), configured in `mkdocs.yml`:

- A translated page sits **next to** its English source: `1-create-bpmn.md` → `1-create-bpmn.zh.md`, `1-create-bpmn.ko.md`
- **Filenames are never translated** — only the locale suffix is added
- Images are shared across languages automatically. **Screenshots stay English** — no localized screenshots, ever
- If a translation is missing or removed, the localized URL serves the English page (fallback). The site never breaks while translations lag behind
- The Material header shows a language switcher with native language names
- Nav labels are translated via the `nav_translations` block under each language in `mkdocs.yml`

---

## English is master: the sync workflow

Every translated file starts with front-matter recording which version of the English source it was translated from:

```yaml
---
source_hash: 3f2a9c1b7e...
---
```

The hash is the MD5 of the English source file at translation time.

**Workflow after editing any English page:**

1. Run the status check:

    ```bash
    python3 scripts/translation_status.py
    ```

    It reports each published page as **current**, **stale** (English changed since translation), or **missing** (no translation yet). Draft pages (not in `mkdocs.yml` nav) are listed as informational only.

2. Run `/sync-translations` to translate missing/stale pages and update hashes. Review the diff before committing.

Never hand-edit a translation without updating the English source — the next sync will overwrite it.

**Drafts:** new exercises and lessons are not translated while in draft. They get translated when published (`/publish-exercise` triggers the sync).

---

## What gets translated — and what never does

### Translate

- Body text, headings, admonition content
- Admonition **titles** (the quoted string): `!!! tip "Plan tip"` → `!!! tip "规划提示"`
- Table content (except keep-English terms below)
- Link text (not link targets)
- Image alt text
- Nav labels (via `nav_translations` in `mkdocs.yml`)

### Keep English — always

| Category | Why |
|----------|-----|
| **Everything the learner types or pastes**: prompts, expressions, variable/argument names, field values, JSON payloads — the full contents of every fenced code block | Must match English screenshots and work identically in the product |
| **UI labels** the learner clicks or reads: "click **Create Agent**", tab names, button text | Screenshots are English; labels must match what learners see |
| **Platform names**: Agent Builder, Maestro, IXP, Action Center, ServiceNow, Studio Web, Data Fabric, Integration Service, Orchestrator | Product names — same rule as English content |
| **Capitalised domain concepts**: Invoice, Purchase Order, Storage Bucket, etc. — when they name a specific artifact the learner creates or selects | They match English UI and data |
| URLs, file paths, filenames, anchors in link targets | Must resolve |
| Front-matter keys and values | Machine-read |

A translated gloss in parentheses is welcome on first use where it helps: "点击 **Create Agent**（创建智能体）".

### Preserve verbatim — markup

- Fenced code blocks, including the language identifier
- Two-column markers: `[[[`, `|30|`, `]]]` (see `Formatting.md`)
- Attribute lists: `{ .screenshot }`, `width="900"`, etc.
- Admonition **type keywords**: `tip`, `info`, `note`, `warning`
- All image paths and link targets
- Bold/emphasis placement mirrors the English source

### In-page anchor links

If an English page links to one of its own headings (`[see above](#some-heading)`), update the anchor in the translation to match the translated heading's slug — or keep the target heading English if it's simpler. Cross-page links need no changes.

---

## Tone per language

The English voice rules in `Language.md` apply in spirit: short sentences, warm, direct, second person. Per language:

### Chinese (zh)

- Simplified characters only
- Address the learner as 你 (not 您) — friendly workshop tone, not formal manual
- Keep sentences short; don't merge English sentences when translating
- Half-width punctuation inside code and technical terms; full-width (，。！) in prose

### Korean (ko)

- Polite formal register: 합니다체 (~합니다/~하세요) — warm but professional, standard for technical guides
- Loanword conventions follow Korean IT usage: 에이전트, 프로세스, 워크플로 등
- Keep particles correct around English terms left in place (Maestro를, Agent Builder에서)

---

## Glossary

Recurring domain terms. Use these consistently; extend the table as new terms appear.

| English | zh | ko |
|---------|----|----|
| agent (AI agent) | 智能体 | 에이전트 |
| agentic automation | 智能体自动化 | 에이전틱 자동화 |
| robot / robotic workflow | 机器人 / 机器人工作流 | 로봇 / 로봇 워크플로 |
| incident | 事件 | 인시던트 |
| invoice | 发票 | 인보이스 |
| purchase order | 采购订单 | 구매 주문(PO) |
| escalation | 升级 | 에스컬레이션 |
| human validation / human-in-the-loop | 人工验证 / 人机协同 | 휴먼 검증 / 휴먼 인 더 루프 |
| workflow | 工作流 | 워크플로 |
| prompt | 提示词 | 프롬프트 |
| exercise | 练习 | 실습 |
| lesson | 课程 | 레슨 |
| step | 步骤 | 단계 |
| You did it! | 大功告成！ | 해냈습니다! |

---

## Adding a locale later

Five edits, and they must land together or the build breaks:

1. **`mkdocs.yml`** — add a language entry under the `i18n` plugin's `languages:` list: `locale`,
   `name`, `build: true`, and a `nav_translations` map. The map is keyed on the *exact* English
   nav labels currently in `nav:`, so it needs one entry per label: `Home`, every `Overview`,
   every `N. Lesson Title`, every `You did it!`, and `Next Steps`. Rebuild it whenever the nav
   changes.
2. **`scripts/translation_status.py`** — add the locale code to `LANGUAGES`. This must stay in
   sync with `mkdocs.yml`; the script is what tells you which pages are stale.
3. **`requirements.txt`** — `mkdocs-static-i18n` is already there. Add `jieba>=0.42` **only for
   `zh`** (it supplies Chinese word segmentation for the search index).
4. **This file** — add the locale's row to the table above, a tone section, and a glossary column.
5. Run `/sync-translations`, then `python3 -m mkdocs build --strict` and spot-check `/<locale>/`.

Cost: the config is minutes; the real cost is one LLM translation pass per page, proportional to
page count. The `source_hash` mechanism bootstraps itself — hashes live in each *translation's*
front-matter and are computed from the English file at translation time, so English pages
authored before localization was enabled need nothing done to them.

## Porting localization to another repository

Everything is additive. Copy:

1. `Master/Localization.md` (this file — adjust glossary/languages)
2. `scripts/translation_status.py`
3. `.claude/commands/sync-translations.md`
4. The `i18n` plugin block from `mkdocs.yml` (rebuild `nav_translations` for that site's nav)
5. The `mkdocs-static-i18n` and `jieba` lines in `requirements.txt`
6. The Localization section of `CLAUDE.md`

Then run `/sync-translations` for the initial translation pass.
