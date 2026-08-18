---
name: setup
description: Initial configuration of the Site Prospector — collects your signature, niches, city and HostGator connection, and installs the local dashboard. Use when the user says "set up prospector", "setup", "start", "my details", or the first time any prospector skill runs without a prospector-config.json.
---

# Prospector — initial setup

Run ONCE. Saves everything in `prospector-config.json` in the project working folder.

## 1. Check config

Look for `prospector-config.json` in the project folder. If it exists, show a summary (WITHOUT the password) and ask what to update. If it does not exist, collect the data below.

## 2. User details (ask in short blocks)

- **Proposal signature**: full name, how you present yourself (e.g. "High-conversion page designer") and WhatsApp `55DDDNUMBER`.
- **Default niches**: suggest nutritionists, psychologists, lawyers, psychiatrists — let them edit.
- **Default city/region**.
- **Leads per search**: default 10.
- **Proposal sending mode**: default "draft email for review".

## 3. HostGator connection

If hosting is already purchased: **do not collect the password through the chat**. Guide the user to fill in the `user`, `domain`, `server` and `password` cPanel fields in `prospector-config.json` (or in the Settings tab of the dashboard). The password lives only in the local file.

## 4. Save

`prospector-config.json` in the project folder:

```json
{
  "signature": { "name": "", "presentation": "", "whatsapp": "" },
  "prospecting": { "niches": ["nutritionists","psychologists","lawyers","psychiatrists"], "city": "", "leadsPerSearch": 10 },
  "sending": { "mode": "draft" },
  "hostgator": { "user": "", "domain": "", "server": "", "password": "", "baseFolder": "clients" },
  "provider": { "name": "", "cpfCnpj": "", "address": "", "cityState": "", "email": "", "whatsapp": "" }
}
```

## 5. Local dashboard

Follow the `leads-dashboard` skill to copy `dashboard-server.py` + the launcher and create the `prospector.db` database and the `dashboard.html`. Explain: double-click `start-dashboard.bat` (Windows) / `start-dashboard.command` (macOS) opens the dashboard at http://localhost:8765 (requires Python in PATH).

## 6. Prerequisites (warn the user)

This toolkit uses two MCP servers:

1. **Browser MCP (Playwright)** — opens leads' websites to assess quality and find the email, and is also the primary source for Google Maps prospecting. Declared in `mcp_config.json` (or add it under your agent's MCP settings).
2. **Prospector CRM MCP** (`prospector_mcp.py`) — manages leads (list, save, status, follow-ups, financials). Declared in `mcp_config.json`.
3. (Optional) **Email MCP/connector** — to create the proposal draft. Without it, the `email-proposal` skill falls back to a compose URL in your browser.

## 7. Wrap up

Confirm what was saved and explain the cycle: **prospect** (skill maps-prospecting) → **redesign** (premium-redesign) → **publish** (hostgator-deploy) → **propose** (email-proposal), with `dashboard.html` as the panel for everything.
