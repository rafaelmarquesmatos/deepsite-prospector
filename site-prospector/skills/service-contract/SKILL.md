---
name: service-contract
description: This skill must be used when generating service contracts for closed clients — website creation/redesign, publishing and maintenance. Trigger when the user says "contract", "generate contract", "formalize", "client closed", "send contract" or asks for the contract (skill service-contract).
---

# Service contract

Generate the draft of the contract for the closed service (redesign + page publishing, with optional maintenance), ready to become a PDF and go by email.

## Data sources (in this order)

1. **Database (`prospector.db`)**: client name, city, closed value, published URL.
2. **Config (`prospector-config.json`)**: PROVIDER data — name, CPF/CNPJ, address, city/state (field `provider`; if it does not exist, collect from the user ONCE and save).
3. **User** (they ask the client): the CLIENT's CPF/CNPJ and address, payment method, deadline, monthly maintenance (yes/no + value).

## Generation

- Template: `references/contract-template.html` — single file with A4 print CSS. Replace all `{{PLACEHOLDERS}}`; check that none are left (search for `{{`).
- Save at `sites/[slug]/contract-[slug].html`. PDF: open in the browser → Ctrl+P → Save as PDF (tell the user this).
- Parameterizable clauses: monthly maintenance (include only if hired) and payment terms (text changes according to the payment method).

## Locked DOCX (the file that goes to the client)

Ready script: `references/generate-docx.py` (requires `python-docx`). Receives `data.json` (same keys as the HTML template + `MAINTENANCE: true/false` and `MAINTENANCE_VALUE`) and generates the .docx with `readOnly` protection + editable regions (`permStart/permEnd`, everyone group) at the client points: CPF/CNPJ and address when they come as "(to fill in)", date and signature — highlighted in yellow. Honest limitation (warn the user once): Word's protection is deterrent — it guides filling but does not stop someone who wants to disable it; for strong validity, use electronic signature (gov.br, Autentique).

## Sending email (draft)

Subject: `Service contract — new page [Business name]`. Body (adapt to the user's voice): thank for the trust, summarize in 2 lines what was agreed (scope + value + deadline), ask them to read the attached draft and reply with an "agreed" (or sign digitally, if the user uses a tool), and close with the config signature. Instruct the user to ATTACH the exported PDF before sending.

## Limits

- ALWAYS keep the footer notice: base draft, review by a lawyer is recommended.
- Do not promise legal validity nor replace formal signature; if the user asks for an electronic signature, suggest uploading the PDF to their tool (gov.br, Autentique etc.).
- Never invent a financial clause: everything comes from the database/user.
