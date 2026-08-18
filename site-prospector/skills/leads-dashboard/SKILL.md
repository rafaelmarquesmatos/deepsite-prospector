---
name: leads-dashboard
description: This skill must be used to create and UPDATE the leads dashboard — the local control panel (SQLite + web page) where the user manages prospects, sites, publications and proposals. Trigger whenever any command from the toolkit changes lead data (skill maps-prospecting, skill premium-redesign, skill deploy, skill email-proposal), or when the user says "dashboard", "panel", "my leads", "client control", "leads database".
---

# Leads dashboard (SQLite + local page)

Architecture at the ROOT of the connected folder:

- **`prospector.db`** — SQLite database, the SOURCE OF TRUTH for leads.
- **`dashboard-server.py` + `start-dashboard.bat` (Windows) / `start-dashboard.command` (macOS)`** — small local server (standard Python, no dependencies). The user double-clicks the .bat → opens `http://localhost:8765` with the full panel: edit, delete and drag cards save straight to the database.
- **`dashboard.html`** — the panel page (generated from the template). Served by the server (database mode) or opened by double-click (file mode: read-only + edits stuck to the browser). The badge at the top shows the mode.

## Setup (once, in initial setup (skill setup) or at first use)

1. Copy `references/dashboard-server.py` and `references/start-dashboard.bat` from this skill to the root of the connected folder.
2. Create `prospector.db` with the schema below (via python3/sqlite3 in the shell).
3. Generate `dashboard.html` from `references/dashboard-template.html` replacing `__DATA__` with the JSON snapshot.
4. Tell the user: "double-click `start-dashboard.bat` opens the panel with the database connected" (requires Python on Windows — if not installed, dashboard.html works in file mode).

## Database schema

```sql
CREATE TABLE IF NOT EXISTS leads(
  slug TEXT PRIMARY KEY, name TEXT, niche TEXT, city TEXT, rating REAL, reviews INTEGER,
  email TEXT, phone TEXT, whatsapp TEXT, oldSite TEXT, reason TEXT,
  status TEXT DEFAULT 'new', newUrl TEXT, proposalDate TEXT, value REAL, notes TEXT,
  contractStatus TEXT DEFAULT 'pending', contractDate TEXT, maintenance REAL, paid INTEGER DEFAULT 0,
  clientDoc TEXT, clientAddress TEXT,
  updated TEXT DEFAULT (datetime('now','localtime')));
```

Status: `new | redesigned | published | proposed | replied | closed | discarded`. `slug` is the key.

## How commands update (ALWAYS the 2 steps)

1. **Upsert into the database** via shell (example):
```bash
python3 - <<'EOF'
import sqlite3
c = sqlite3.connect('PATH/prospector.db')
c.execute("INSERT INTO leads (slug,name,status,...) VALUES (?,?,?,...) ON CONFLICT(slug) DO UPDATE SET status=excluded.status, updated=datetime('now','localtime')", (...))
c.commit()
EOF
```
   - `skill maps-prospecting` → inserts leads (`new`) and discarded (`discarded`, reason in `notes`). NEVER overwrite a lead whose status has already advanced.
   - `skill premium-redesign` → `status='redesigned'` · `skill deploy` → `status='published'`, `newUrl` · `skill email-proposal` → `status='proposed'`, `proposalDate`.
   - User reports replied/closed → `status='replied'|'closed'`, `value` (+ `maintenance` if there is a monthly fee).
   - `skill service-contract` → `contractStatus='sent'` + `contractDate`. Client signed → `contractStatus='signed'`. Payment received → `paid=1`.
2. **Regenerate the snapshot**: read all leads from the database and rewrite `dashboard.html` from the template with the updated embedded JSON (`{"updated": "...", "leads": [...]}`) — it is the fallback for anyone opening without the server.

If the database does not exist yet (old user), create it and import the leads from the snapshot embedded in the current `dashboard.html` before the upsert. Respect user edits: before rewriting a lead, read the current record from the database.

## What the panel does on its own (do not reimplement)

Kanban drag & drop, modal editing, deletion, search, automatic pagination, funnel, follow-ups (proposal 4+ days), closed/potential revenue, Contracts view (pending/sent/signed status + document link + paid) and Financials view (received, to receive, maintenance MRR, 12-month projection) — all in the template. The toolkit only keeps the DATABASE correct and the snapshot up to date.
