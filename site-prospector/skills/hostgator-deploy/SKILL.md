---
name: hostgator-deploy
description: This skill must be used when publishing pages to HostGator hosting — upload via the local automatic publisher script, FTP or cPanel, per-client folder creation, public URL and HTTPS verification. Trigger when the user says "publish", "upload the site", "put it live", "deploy", "hostgator" or asks to publish (skill hostgator-deploy).
---

# HostGator deploy

Publish pages to `public_html/[baseFolder]/[slug]/` and make sure the public URL `https://[domain]/[baseFolder]/[slug]/` works.

## Credentials

Everything comes from `prospector-config.json` (the `hostgator` block): `user`, `domain`, `server`, `password`, `baseFolder` (default `clients`). **The password lives ONLY in that file, on the user's computer — it is never typed into the chat, never shown in any output, log or command shown to the user.** If the password is empty, guide the user: dashboard → Settings tab → HostGator connection → paste the password and save (or edit the file by hand). Never through the chat.

## Method 1 — Local automatic publisher (RECOMMENDED: install once, never click again)

The assistant's sandbox network usually CANNOT reach FTP or cPanel — this applies to every user. Publishing runs on the user's machine via a publisher installed in the Windows Task Scheduler: every minute it checks the queue and uploads whatever is there, hidden, reading credentials from the config. The user installs ONCE and the hostgator-deploy skill becomes 100% automatic.

1. **Ensure the publisher files are in the connected folder** (copy from `references/` of this skill, overwriting old versions), according to the user's OS — ask or detect:
   - **Windows**: `publish-now.ps1`, `publish-now.bat`, `hidden-publisher.vbs`, `install-publisher.bat`.
   - **macOS**: `publish-now.command` and `install-publisher.command` (the installer registers the publisher in launchd, every 60s; uninstall = `launchctl unload` of the com.prospector.publisher plist).
   In doubt, copy all — each system ignores the ones for the other.
2. **First time**: ask for ONE double-click on `install-publisher.bat` (Windows — creates the "ProspectorPublisher" task; permission error = right-click → Run as administrator) or `install-publisher.command` (macOS — if macOS blocks it for security: right-click → Open on first run). Only once ever.
3. **Build the queue**: write `publish-queue.txt` at the root of the connected folder, one file per line: `local/path/file.html|public_html/[baseFolder]/[slug]/index.html`. Include the page (`index.html`) and the cover (`proposal.html`) of each client. Within 1 minute the publisher uploads everything by itself and renames the queue to `publish-done-[date].txt` (the log stays in `publisher-log.txt`).
4. **Wait ~90s and verify**: check that the queue was renamed and test the URLs (verification below). Without an installed task, the manual fallback is the double-click on `publish-now.bat` (Windows) or `publish-now.command` (macOS).

## Method 2 — FTP direct from the sandbox (try first, silently)

Before involving the user, try publishing yourself: `curl -sS --connect-timeout 15 -T [file] "ftp://[server]/public_html/[baseFolder]/[slug]/index.html" --user "[user]:[config password]" --ftp-create-dirs` (password read from the file via script — never shown). If it works, great: zero user action. If the sandbox network blocks it (timeout/refused), fall WITHOUT DRAMA to Method 1 — do not insist with repeated attempts.

## Method 3 — Browser (last resort)

If methods 1 and 2 fail (e.g. curl missing on the user's machine): cPanel File Manager via the browser MCP (Playwright) — the USER does their own login (never ask for the password in the chat), you navigate, create the folders and upload through the interface.

## Verification (mandatory, after any method)

1. Open `https://[domain]/[baseFolder]/[slug]/` and the cover `.../proposal.html` — confirm they load with the right content.
2. **HTTPS mandatory**: must load with a valid padlock. If there is a certificate error: HostGator has free SSL — guide: cPanel → **SSL/TLS Status** → select the domain → **Run AutoSSL** (minutes). Until HTTPS validates, the publication is NOT complete — an `http://` link NEVER goes to a client.
3. Update `leads.md` + dashboard with status `published` and the URL.

## Connection test from initial setup (skill setup)

Publish a simple `test.html` ("It works!") at `public_html/[baseFolder]/test/index.html` via Method 2; if blocked, leave the Method 1 scripts copied in the folder, build the queue with the test and ask for the 2 clicks — this teaches the user the flow right in setup.
