# Prerequisites

## What's a coding agent?

A coding agent is an AI assistant that understands a goal described in plain English, explores your codebase, and builds working components — not just autocomplete. You stay in control: you review its work and steer it as you go.

### Examples

- **Claude Code**
- Codex CLI
- Cursor
- Gemini CLI
- GitHub Copilot Agent

!!! tip "This course uses Claude Code"

### The mental model

| Concept | Definition |
| :--- | :--- |
| **Tools** | Built-in actions the agent can take: read a file, run a bash command, search the web, edit code. |
| **Skills** | Domain knowledge bundles the agent loads when it sees a matching task — a playbook for one thing. |
| **Commands** | Manual shortcuts you type: `/commit`, `/test`, `/deploy`. Triggered by you, not the agent. |
| **Hooks** | Run automatically at lifecycle events — before an edit, after a commit, on session start. Used for guardrails. |
| **Subagents** | Specialised workers spawned by the main agent, used to parallelise or isolate complex tasks. |
| **Plugin** | A package that bundles any of these together — like a Marketplace app for your coding agent. |

### Skills

A **Skill** is a folder — sitting in `.claude/skills/` (or equivalent) — with a `SKILL.md` file inside. The agent reads each `SKILL.md`'s description, and when your prompt matches, it loads the full skill on demand.

A skill can bundle more than instructions: reference docs, code patterns, helper scripts, even binaries. It also declares which tools it's allowed to use.

Every `SKILL.md` file is built from four parts:

| Part | Purpose |
| :--- | :--- |
| **Frontmatter** | Declares the skill's name, description, and allowed tools |
| **Discovery prompt** | The description field that triggers automatic skill loading |
| **Instructions** | Step-by-step guidance the agent follows when active |
| **References** | Paths to supporting files like API docs and code patterns |

```markdown title="Example SKILL.md"
---
name: uipath-coded-agents
description: Scaffold, build, run, evaluate, and deploy UiPath coded agents...
allowed-tools: [Read, Edit, Bash(uip:*), Bash(uipath:*)]
---

# How to build a UiPath coded agent

When the user asks for a new coded agent:

1. Run `uipath new --framework langgraph`
2. Create agent.py following the pattern in references/
3. Add an evals/ folder with at least 5 test cases
4. Run `uipath eval` before deploying

## References
- references/sdk-methods.md
- references/langgraph-patterns.md
```

## Coding Agents and UiPath

UiPath ships a plugin for Claude Code. It bundles skills, hooks, and references — giving the agent domain knowledge about UiPath products out of the box.

The plugin contains three components:

| Component | Details |
| :--- | :--- |
| **10+ skills** | Domain knowledge for every UiPath product: `uipath-agents`, `uipath-coded-apps`, `uipath-rpa`, `uipath-maestro-flow`, `uipath-platform`, `uipath-test`, and more. |
| **1 subagent** | `uipath-project-discovery-agent` — auto-runs on first contact with a UiPath project and builds context for the agent. |
| **Hooks & references** | Session-start nudges, activity docs, and allowlists for safe read-only commands. |

### The UiPath skill catalog

The plugin provides skills across the UiPath platform, including:

| Skill | Description |
| :--- | :--- |
| `uipath-agents` | Scaffold, build, run, evaluate, and deploy coded agents (LangGraph, LlamaIndex, OpenAI Agents) |
| `uipath-rpa` | Generate and edit RPA workflows (XAML) for Studio Desktop with a discovery-first approach |
| `uipath-coded-apps` | Push/pull TypeScript + React apps to Studio Web, pack & publish to Orchestrator |
| `uipath-solution` | Create and deploy solutions |
| `uipath-maestro-flow` | Create, validate, and debug UiPath Flow projects using the `.flow` JSON format |
| `uipath-platform` | Auth, Orchestrator management, solution lifecycle, Integration Service, CLI tools |
| `uipath-test` | Generate, run, and maintain automated test suites for UiPath projects |
