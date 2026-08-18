---
name: premium-redesign
description: This skill must be used when redesigning the website of a prospected client — creating a new, premium, high-conversion version of the existing page, keeping the client's content, logo and palette. Trigger when the user says "redesign site", "improve page", "redo the client's site" or asks to redesign (skill premium-redesign).
---

# Premium page redesign

Create a NEW VERSION of the client's page — not a brand-new page. The client must recognize their own business, only elevated to the standard their revenue deserves.

## Non-negotiable rules

1. **No FACT invented — but the text MUST be improved.** Every service, credential, number, address and contact comes from the original site (or from the Google profile). No fictional data, no invented testimonials, no services the client does not offer. However, the TEXT is not pasted raw: rewrite with better copy — stronger headlines, clearer sentences, reading hierarchy — always saying the same truth the original says.
2. **Original photos and logo are MANDATORY on the new site.** Every usable photo from the existing site (professional, office, logo) must appear on the new page, via the original URLs (collect via `img.currentSrc` in the browser, scrolling the whole page to beat lazy-loading). The client must recognize themselves instantly.
3. **Identity preserved.** Keep the client's logo, color palette and photos. If the original palette is weak (e.g. pure saturated colors), refine the tones — never change the color family.
4. **More complete than the original.** The new site must be MUCH more professional and well structured. If the original has few sections, CREATE the relevant missing sections — as long as they are filled only with real information: social proof (rating + real Google reviews), "how the service works" (if deductible from the original), location with map, opening hours (from the Maps profile), FAQ with questions answerable by real content. A section that would require inventing a fact = do not create it.
5. **Single file.** `sites/[slug]/[slug].html` self-contained: inline CSS in the `<head>`, no build step, no dependencies beyond Google Fonts.
6. **TOTAL responsiveness (non-negotiable).** The page will be viewed on the client's phone AND inside the cover page frame (~1000-1500px). It must be perfect at ANY width: 360, 375, 768, 1024, 1280 and 1440px — no horizontal scroll, no text overflow, no stretched image, no broken section at any of these points. Use fluid grid/flex, `clamp()` for typography and breakpoints tested one by one. A page that breaks at any width is NOT delivered.
7. **Editor always.** Every redesign also generates `sites/[slug]/[slug]-editor.html` (the editing layer from `references/visual-editor.md`) — never deliver a page without the editable version.
8. **Comparator always.** Every redesign batch ends with `compare.html` at the root of the connected folder, generated from `references/comparator-template.html` (replace `__CLIENTS__` with the JSON array; merge with existing clients). The standard delivery for each client is 3 files: page + editor + a tab in the comparator.

## Page structure (adapt to the profession)

1. **Hero**: name + specialty, a clear one-line promise, primary CTA (WhatsApp) visible without scrolling, photo of the professional/clinic.
2. **Social proof**: Google rating in prominence ("5.0 ★ · 121 Google reviews") — it is real and verifiable. Quote 2-3 real Google Maps review excerpts if collected.
3. **Services/areas**: clickable cards — each card goes to the detailed section anchor or straight to WhatsApp with a pre-filled message (`https://wa.me/55DDDNUMBER?text=Hello! I came from the site and want to know about [service]`).
4. **About**: real credentials and background (build authority — never cut).
5. **Structured offer** (when it makes sense): turn "book an appointment" into engagement options (e.g. single session, 90-day follow-up, six-month plan) — NO prices, only names and what they include, all leading to WhatsApp. Only create plans that are an obvious grouping of the already-offered service.
6. **Location and contact**: address, map (Google Maps iframe), opening hours, phone, socials.
7. **Footer**: professional data (class registration if present in the original).

## Copywriting (improve without inventing — rewriting is mandatory)

The new site's text is NEVER the old site's text pasted. Rewrite everything with technique, saying only what the client already says/offers:

- **Hero headline = benefit, not label.** "Sports nutrition in SP" is a label; "Your training deserves results that show" is a headline (with the label becoming a kicker/subtitle for SEO).
- **Soft PAS structure** across the page: touch the audience's real pain, show the path, present the service as the solution — in the niche's tone, without launch-aggressiveness.
- **Scannability**: nobody reads an 8-line paragraph. Break into 2-3 line blocks, verb-led bullets, subtitles that tell the story on their own (someone who only reads the titles understands the page).
- **1 CTA per fold**, always action- and benefit-oriented ("I want my assessment" > "Click here"), all to WhatsApp with contextual pre-filled message.
- **Social proof woven in, not stacked**: Google rating near the CTA, real quote near the section it refers to.
- **Microcopy**: captions under buttons ("reply within minutes"), human labels on forms and sections.
- Forbidden: empty clichés ("quality and commitment", "excellence in service") without a fact to back them; invented superlatives; result promises the client does not make.

## Structural quality bar (the "real professional")

The finished page must look like it was made by a design studio — honest test: placed next to a premium template of the niche (high-end clinics/offices), it cannot owe anything. That means: consistent grid (same spacing between ALL sections), impeccable alignment, rhythm alternation between sections (light/dark/accent background, full/contained width), images with coherent treatment (same border radius, same temperature), typography with at most 2 families and a harmonic scale, and no "orphan" section that looks pasted from another site.

## Aesthetic standard

- Typography: an elegant serif for headings (Playfair Display, Fraunces, Lora) + a clean sans for body (Inter, Sora, DM Sans), weights 400/600. Strong hierarchy: h1 ≥ 40px desktop / 30px mobile.
- Generous spacing: sections with 80-120px vertical breathing room on desktop; nothing cramped.
- Palette: 1 brand color + warm neutrals + 1 accent tone for CTA. AA contrast at minimum.
- Floating WhatsApp button fixed at the bottom right.
- Premium micro-touches: 12-16px borders, soft shadows, 0.2s hover transitions. No carousels, no heavy animations, no JS beyond the essentials.
- Speed: the page must open instantly — no libraries, no fonts beyond 2 families.

## Final checklist (mandatory before delivery)

- [ ] Zero placeholder text / lorem ipsum
- [ ] All links and CTAs point to the client's REAL contact
- [ ] WhatsApp number in correct wa.me format (55 + area code + number)
- [ ] Responsive verified at 360, 375, 768, 1024, 1280 and 1440px — zero horizontal scroll and zero breakage at ALL
- [ ] Title and meta description filled with name + specialty + city
- [ ] Comparison with the original: all important content from the old site is present
- [ ] Client's ORIGINAL logo and photos present on the new page
- [ ] `[slug]-editor.html` generated and `compare.html` updated

## Visual editor and comparator

The visual editing layer (to generate `[slug]-editor.html`) is in `references/visual-editor.md` — inject the script exactly as documented there. The before/after comparator is in `references/comparator-template.html` — replace `__CLIENTS__` with the JSON array and save as `compare.html` at the root of the connected folder (merging with existing clients).
