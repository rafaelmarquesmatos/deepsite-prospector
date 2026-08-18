# Site Prospector

Semi-automated client prospecting for businesses with weak websites: find high-potential businesses on Google Maps, build them a premium redesign, publish it on HostGator, and send a proposal by email — all driven by an AI assistant through natural language.

**Agent-neutral.** This is a portable skills + MCP toolkit, not a plugin tied to any vendor. It works with any AI agent/IDE that supports **MCP servers** and **skills** (Claude Code / Claude Cowork, Gemini CLI / Antigravity, Cursor, Codex, opencode, and others). The CRM, the dashboard, and the templates are plain Python/SQLite/HTML with zero agent-specific dependencies.

The business search runs in the **browser** (Playwright MCP) — no Google API key required, no vendor lock-in. A browser is used only to evaluate each lead's website and find the email.

## Toolkit layout

```
site-prospector/               ← this folder is the toolkit
├── mcp_config.json            defines the MCP servers (CRM + Playwright browser)
├── prospector_mcp.py          CRM MCP server (SQLite)
├── dashboard/                 local dashboard (Python/SQLite) — ready-to-copy
└── skills/                    the 7 skills (SKILL.md)
    ├── setup/
    ├── maps-prospecting/
    ├── premium-redesign/
    ├── email-proposal/
    ├── hostgator-deploy/
    ├── leads-dashboard/
    └── service-contract/
```

## Installation

### 1. Register the MCP servers

Register the two MCP servers from `mcp_config.json` in your agent's MCP configuration:

- **prospector-crm** — the local CRM server (`prospector_mcp.py`). Point `--folder` at your project folder (where `prospector.db`, the leads and the sites live).
- **playwright** — the browser automation server (`@playwright/mcp`), used to prospect on Google Maps, evaluate client websites, and find emails.

Every agent has its own MCP config location (check your agent's docs). The JSON schema is the standard MCP one, so it's the same for all of them.

### 2. Install the skills

Copy the `skills/` folder into your agent's skills directory so the assistant can load them on demand:

- **Claude Code:** `~/.claude/skills/`
- **Gemini / Antigravity:** `~/.gemini/skills/` (or `.agents/skills/` in the project)
- **opencode:** `.opencode/skills/` in the workspace root
- **Cursor:** check Cursor's skills/rules docs for your version

The skills are plain `SKILL.md` markdown with YAML frontmatter — the same format most agents use. If your agent uses a different convention, adapt the folder layout only; the content is the logic.

### 3. Configure the Prospector

Open the project folder and tell the assistant **"set up the prospector"**. The `setup` skill collects your details, the HostGator connection, and installs the local dashboard.

## How to use (natural language)

1. **"Prospect nutritionists in São Paulo"** → browses Google Maps, qualifies (high rating + weak site + email), and fills the dashboard.
2. **"Redesign the top 5"** → premium redesign + visual editor + before/after comparator.
3. **"Publish to HostGator"** → uploads pages and the cover page, verifies HTTPS.
4. **"Send the proposal"** → anti-spam email draft ready to review.
5. After that: contract, and the `dashboard.html` manages everything (kanban + financials).

## How it stays agent-neutral

- **No vendor plugin files** — only standard MCP config, Python, SQLite, HTML, and `SKILL.md` files.
- **No hardcoded agent paths** — paths are placeholders you fill in for your machine and project folder.
- **Browser-based Google Maps search** — no Google Maps Platform API key required.
- **Local CRM + dashboard** — all data lives in your computer's `prospector.db`; nothing depends on a cloud connector.
- **Any email provider** — the proposal skill drafts via your email MCP/connector or a plain compose URL.

## Notes

- Currency is shown as `R$` (BRL) — the workflow targets the Brazilian market (HostGator hosting, WhatsApp as the primary contact channel). Adjust the templates if you operate elsewhere.
- The `dashboard.html` is a single self-contained panel: kanban drag & drop, editing, funnel, contracts and financials. Double-click `start-dashboard.bat` (Windows) / `start-dashboard.command` (macOS) to run it with the live database.
