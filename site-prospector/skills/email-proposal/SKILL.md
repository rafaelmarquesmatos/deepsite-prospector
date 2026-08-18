---
name: email-proposal
description: This skill must be used when writing and sending the commercial proposal email to a prospected lead — an email presenting the new version of the site, with rapport and no price. Trigger when the user says "send proposal", "email the client", "send the site to the client" or asks to send the proposal (skill email-proposal).
---

# Email proposal

The email does NOT sell — it sparks curiosity and proves work done. The close (price, scope, meeting) happens in the reply. An email that looks like a salesperson dies in spam; an email that looks like a person who already worked for free for the recipient gets opened and answered.

## Principles

1. **Rapport first.** Open with a SPECIFIC, verifiable compliment: the Google rating, a real review quoted, a credential from the site. Never a generic compliment.
2. **The pain without offense.** Point out 1-2 objective flaws of the current site as an opportunity ("I noticed the site is hard to read on mobile"), never as criticism of the professional.
3. **Proof before ask.** The work is ALREADY done and live. The link is the proposal.
4. **Zero price.** Price only in the conversation the reply opens.
5. **Zero pressure.** No false urgency, no "last spots". A single CTA: take a look and reply with your thoughts.
6. **Short.** 120-180 words. A busy professional does not read a long email from a stranger.

## Structure

- **Subject**: personal, specific question, ≤ 60 characters, no marketing look. E.g.: `Dra. [Name], can I show you something about your site?` or `I prepared something for [Clinic X]`.
- **Paragraph 1**: who found you + specific compliment (reviews/credential).
- **Paragraph 2**: observation about the current site (1-2 objective points).
- **Paragraph 3**: "I prepared a new version, already live" + THE ONLY LINK of the email: the cover page (`.../proposal.html`), which shows before and after side by side. If the cover does not exist, link the new page directly.
- **Paragraph 4**: CTA — also open it on your phone, reply with your impression.
- **Signature**: name, presentation and WhatsApp from the config (a complete signature humanizes and reduces suspicion).

## Anti-spam checklist (BLOCKING — run before creating the draft)

Review the finished email against EVERY item; if it fails any, rewrite before creating the draft:

- [ ] **1 link only** (the cover page). Two at most if including the old site — never more than that.
- [ ] **No URL shortener** (bit.ly and the like = certain spam). The link is the real domain, with `https://`.
- [ ] **Link as an HTML anchor with clean visible text.** Most webmail providers wrap every link in their own redirect (`google.com/url?q=...`) on save — you cannot prevent it, and in a plain-text body the wrapper becomes VISIBLE, which looks like a scam. That is why the draft is created with an HTML body and the link as an anchor: `<a href="https://[domain]/[baseFolder]/[slug]/proposal.html">https://[domain]/[baseFolder]/[slug]/proposal.html</a>` — visible text = the clean URL built from the config (never copied from another email). After creating it, check the draft: the visible text must start with `https://[config domain]`.
- [ ] **Clean, human domain.** If the config domain is a technical/temporary subdomain (full of numbers, like `name1783367206076.1711244.somehost.com.br`), STOP before sending any proposal: a link like that looks like a scam and kills the trust the cover builds. Guide the user to activate their own domain (free on most hosting plans: cPanel → Domains, or a registrar) and update the `domain` field in the dashboard Settings. A proposal only goes out with a presentable domain.
- [ ] **No trigger words**: free, promo, unmissable, offer, discount, click here, 100%, guaranteed, urgent.
- [ ] **No ALL CAPS in the subject, no "!!", no emoji** in the subject.
- [ ] **Plain text** — minimalist HTML body (only paragraphs and the link anchor; zero colors, buttons, images or attachments) (an attachment from a stranger raises the spam score AND the fear of opening; the cover link replaces the preview).
- [ ] **Subject ≤ 60 characters**, phrased as a question or personal sentence with the business name.
- [ ] **First line 100% personalized** (name + a real fact from the reviews) — spam filters and humans recognize generic templates.
- [ ] **Sender = the user's own active email account** (reputable providers already have SPF/DKIM). Never suggest mass sending: sends are 1 to 1, a few per day — human pattern.

## Sending

- **Draft mode** (default): create via the user's email MCP/connector (draft tool) or via the provider's compose URL (`https://mail.google.com/mail/?view=cm&fs=1&to=...&su=...&body=...` for Gmail; equivalent for other providers) with recipient, subject and body ready. Warn the user to review before sending.
- **Send-direct mode**: if the connector supports sending, send it; otherwise open the webmail via the browser MCP (Playwright) or create the draft and warn.
- Never send to a lead without a confirmed email; in those cases, suggest contacting via WhatsApp with the same message adapted.

## Cover page (what the client sees on click)

The email link leads to the cover page generated in `deploy` (template in `references/proposal-cover-template.html`): client name at the top, before/after side by side and the user's signature. It exists to give the click credibility — the client sees their own business, not a strange link. Requirements: served over `https://`, personalized with real data, no request for personal data.

## After sending

Record in the database/`leads.md` (status + date) and in the dashboard. Replies are checked by the command "check email replies" (via the email connector) — suggest the user schedule a daily check. Follow-up via "proposal follow-ups" after 3+ business days without a reply (1 single follow-up per lead: short, gentle, "did you manage to see the page?").
