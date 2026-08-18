---
name: deploy
description: Publish a redesigned site to the user's own hosting — prepare the files, guide a manual upload (any provider), verify the live HTTPS URL, and record the published status. Trigger when the user says "publish", "deploy", "put it live", "upload the site" or asks to publish (skill deploy).
---

# Deploy

Publish `sites/[slug]/[slug].html` (and its `-editor.html`) to the user's hosting, at `https://[domain]/[baseFolder]/[slug]/`, then verify **HTTPS** before sharing with a client.

## Hosting is provider-agnostic and manual-first

There is no provider lock-in. The user uploads the files themselves through whatever they already use — cPanel, Plesk, an FTP client, Netlify, Vercel, any host. The assistant prepares everything and verifies the result; it never handles hosting credentials.

## What you need

- **`domain`** — the public domain the site will live on (e.g. `example.com`). Read from `prospector-config.json` (`hosting.domain`) or ask the user.
- **`baseFolder`** — the subpath under the domain (default `clients`), so the page ends up at `https://[domain]/[baseFolder]/[slug]/`. Read from `hosting.baseFolder` or default to `clients`.

## Flow

1. **Prepare the files.** In `sites/[slug]/`, ensure there is an `index.html` (the redesigned page) — rename `[slug].html` to `index.html` if needed so the URL works without a filename. Keep `[slug]-editor.html` and, when the proposal step will need it, the proposal cover (`proposal.html`).
2. **Tell the user what to upload.** Print a short, concrete checklist: upload the contents of `sites/[slug]/` into `[baseFolder]/[slug]/` on their hosting (usually under `public_html/` or `www/`), so `index.html` sits at `https://[domain]/[baseFolder]/[slug]/index.html`.
3. **Wait for the user** to confirm the upload is done (or to give you the resulting URL). Do not invent a URL.
4. **Verify (obligatory).** Fetch `https://[domain]/[baseFolder]/[slug]/` with the browser/web tool and confirm it serves the redesigned page over **HTTPS** (padlock, no mixed content, no redirect to `http`).
5. **Record.** Set the lead's status to `published` and `newUrl` to the confirmed HTTPS URL, then refresh `leads.md` + `dashboard.html`.

## Rules

- **HTTPS only.** An `http://` link never goes to a client.
- **Real domain only.** A numeric/temporary subdomain (e.g. `name1234.somehost.com`) stops the proposal until the user points a proper domain.
- **Never invent a URL.** Record a URL only after the user confirms it or verification succeeds.
- The assistant never asks for or touches hosting credentials — the user performs the upload themselves.
