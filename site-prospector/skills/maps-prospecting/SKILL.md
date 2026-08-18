---
name: maps-prospecting
description: This skill must be used when prospecting clients on Google Maps — finding well-rated businesses with weak websites, qualifying leads, assessing the quality of third-party sites and building the leads list. Trigger when the user says "prospect", "find clients", "get leads", "clients with bad sites" or asks to prospect (skill maps-prospecting).
---

# Google Maps prospecting

Find the golden client: a business that ALREADY earns well (high rating, many reviews) but loses clients because of a weak website. You are not creating demand — you are fixing where the money is leaking.

## Flow — browser-based search, browser-based assessment

The business search uses the **browser MCP (Playwright)** — it works on any agent with a browser tool, with no Google API key or vendor plugin required. The same browser is used to assess the site and hunt for the email.

1. **Search for the businesses:** open `https://www.google.com/maps`, search `[niche] in [city]` and, for each profile, read the name, rating, number of reviews, website, phone and address.
   - **Filter 1 — financial potential**: `rating` ≥ 4.7 AND `reviews` ≥ 40. Failed → move on.
   - **Filter 2 — HAS its own website**: needs a `website` field that is NOT Instagram/Facebook/Linktree/third-party directory. No site or social media only → discard (record the reason) and continue.
2. **Assess the site + find the email (browser):** for each candidate that passed filters 1 and 2, open the `website` with the browser MCP and:
   - **Filter 3 — weak site**: assess by the criteria below. Good site → discard. Active but weak site → candidate.
   - Look for the public email (mandatory — see below) and WhatsApp.
3. Stop when the qualified-lead target is reached (config, default 10) or after assessing 25 establishments.
4. Skip establishments already in `leads.md` (assessed in previous searches).

## Weak-site criteria (record the specific reason)

Qualifies as a lead if the (active) site has 2 or more of these problems:

- Dated layout (looks like a 10+ year old template, system fonts, stretched/pixelated images)
- No clear CTA for booking/contact (no WhatsApp or agenda button visible in the first fold)
- Free domain or hosted on a third-party platform (Google Sites, free Wix, third-party subdomain with the platform's branding)
- Not responsive (breaks on mobile)
- Disorganized content: services hidden, no hierarchy, run-on text without sections
- No social proof (no review/testimonial, despite the high rating on Google)

The recorded reason must be objective and verifiable — it will be quoted in the proposal. E.g.: "domain redirects to free Google Sites, basic template, no booking CTA".

## Data collected per lead

Name, rating, number of reviews, phone, WhatsApp, email, site URL, reason.

**WHATSAPP: always capture, separate from phone.** Sources, in order: WhatsApp button/link on the lead's site (look for `wa.me/`, `api.whatsapp.com` or a WhatsApp icon — extract the number from the link); the mobile number from the Maps profile (Brazilian numbers with a 9th digit are mobile — assume WhatsApp). Record in international format `55 + area code + number` (e.g. `5511999990000`), ready for `wa.me`. WhatsApp feeds the dashboard buttons and the plan B contact when the email does not answer.

**EMAIL IS MANDATORY.** The proposal goes by email — a lead without a public email does not close the loop. Look in this order: site (footer and contact page), `mailto:` links, home page of the clinic/office where they practice, Google search for "[name] + email/contact". If NO email is found: **discard the lead, record it in the discarded list (with whatever contact exists, e.g. WhatsApp/Instagram) and keep searching for the next one** until the target is met. Note: a "site" that points to a third-party directory (localtreino, acheioprofissional etc.) does not count as their own site — discard at Filter 2.

## Output — local CSV + leads.md

Primary destination: a **local CSV** file (e.g. `leads-[niche]-[city].csv`, UTF-8 with BOM so it opens correctly in Excel) with all collected leads, both qualified and discarded, ranked by potential (high rating + worse site). Tell the user where the file is.

Working copy `leads.md` (same columns) for status control:

```markdown
| # | Name | Rating | Reviews | Email | Phone | Current site | Reason | Status | New URL |
```

Possible statuses: `new`, `redesigned`, `published`, `proposal sent`. When a status changes (redesign → publish → propose), update `leads.md` and refresh `dashboard.html` (skill `leads-dashboard`). Never overwrite old leads — only append and update.

> If your agent has a spreadsheet connector (e.g. Google Sheets, Excel Online) you may additionally sync the CSV to a shared sheet and give the user the link. That is optional — the CSV is the source.

## Good practices

- Working by region is an advantage: less competition in the offer and local knowledge.
- While the browser is working, do not interrupt the flow with questions — just report the final table.
- If Google Maps asks for login/captcha, pause and warn the user.
