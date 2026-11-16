# Smartline Point Cleaning Hub Ltd — project notes

## Client
Smartline Point Cleaning Hub Ltd — commercial, residential, post-construction
cleaning and landscaping. Established 2018.
ICIPE Road, Sports Drive, Suite 8, Kasarani · P.O. Box 48018-00100, Nairobi
+254 711 128736 · info@smartlineltd.co.ke · domain wanted: **smartlineltd.co.ke**
Source material: `smart.pdf` (their current 5-page company profile).

## Quotation — settled figures (AMM-Q-2026-187, 16/11/2026; no validity period stated)
| Item | KES |
|---|---|
| Website — full build (design, dev, content, Google set-up, company profile, launch) | 35,000 |
| Domain .co.ke — 1 year | 2,000 |
| Server space + company email — 1 year | 3,000 |
| **Total** | **40,000** |

Payment: 40% of the build (14,000) + domain + hosting = **19,000 to start**;
**21,000 on go-live**. Renewal from year two: **3,000/yr flat** (domain + server space).
M-Pesa Send Money 0792 507 750 (Allen Muraya Maina), ref SMARTLINE.

Emails included in hosting: info@, accounts@, operations@, marketing@ plus any
others the client needs, at no extra cost.

Settled wording — do not re-litigate:
- Build timeline **14–21 days** from deposit.
- **No revisions clause** (removed at client-facing request).
- Support is **constant and included**, no 30-day window.
- **No validity/expiry date** on the quote.
- Scope includes **social media launch posts** (Facebook, Instagram, LinkedIn, WhatsApp).
- Website description is written technically (hand-coded HTML5/CSS3/JS, WebP + lazy loading,
  LocalBusiness schema, CSP/HSTS, sitemap + robots).
- **No signatory/acceptance block** — page 2 closes with a one-line call to action.
- Page 2 carries a value section ("What this buys the business") framing the spend as investment.

## Repo
https://github.com/murayaallen/Smartline-Point-Cleaning-Hub-Ltd — branch `main`.
**Public by Allen's choice (16/11/2026)**, including the quotation PDF (KRA PIN,
M-Pesa number, client pricing) and the client's profile and share card. Do not ask again;
do not add anything more sensitive than that (bank statements, IDs, registers) to this repo.

## Files
- `make_quotation.py` — ReportLab generator, single source of truth for the
  figures with `verify()` on import. Re-run it to regenerate the PDF.
- `Smartline Point Cleaning Hub - Website Quotation.pdf` — 2-page A4 quotation.
- `PLAN.md` — domain, sitemap, design direction, build plan, timeline.
- `brandkit.py` — shared ReportLab house style (palette, fonts, logo mark, masthead, footer).
- `make_choices.py` / `Smartline Point Cleaning Hub - Domain & Choices.pdf` — one-page
  tick-sheet sent to the client: 6 available domain names (recommendation flagged) plus
  client-naming, pricing-display and WhatsApp-number decisions. Ref AMM-D-2026-187.
  Note: run these scripts with plain `python`, not `python -I` (brandkit import).

## Status
Quote **accepted** (16/11/2026). Planning stage — see `PLAN.md`.

## Domain — SETTLED
- **Client chose `smartlinepointcleaning.co.ke`** (16/11/2026). Register this.
  Emails: info@ / accounts@ / operations@ / marketing@ **@smartlinepointcleaning.co.ke**.
- Their printed profile still shows smartlineltd.co.ke → the profile reprint is now
  mandatory (already inside the quoted scope). smartlineltd.co.ke is still free if they
  ever want it as a redirect.
- **smartline.co.ke is TAKEN** by another party (KWE/Shujaahost, exp. 07/04/2027).
  Do not print or chase it.
- Also free if a defensive second name is wanted: smartlinecleaning.co.ke,
  smartlinecleaners.co.ke, smartlinepoint.co.ke, smartlinehub.co.ke.
- Canonical: https://smartlinepointcleaning.co.ke (apex), www 301s to apex.

## Client brand colours (sampled from their profile PDF)
Navy `#121439` · indigo `#2E2482` · orange `#F98719` · white.
Tagline: *Assuring you the best*. Logo is a stylised S, indigo with an orange swoosh.

## Logo — round 2 is the live one
Round 1 (`logo_concepts.py`, flat SVG marks) was **rejected by Allen as childish**:
uniform round-capped strokes, cartoon sparkles, saturated orange. Do not revive it.

Round 2 = `logo_premium.py` + `make_logo_premium.py` →
`Smartline Point Cleaning Hub - Logo Concepts Rev B.pdf` (6 pages, ref AMM-L-2026-187 rev B):
01 The Seal · 02 The Plate · 03 The Letter · 04 The Cipher · 05 The Droplet · 06 The Stamp.

What makes it premium — keep these rules for anything else in this identity:
- letterforms from **Bodoni MT**, never drawn blobs; **Copperplate Gothic** tracked for
  the wordmark; Bodoni italic for the tagline
- flat cut terminals, no rounded caps anywhere
- hairlines (0.3–0.6pt), double-rule borders, engraved rings
- palette: ink navy `#0E1430`, indigo `#241E63`, **brass `#B8862F`** (not orange),
  paper `#FAF8F4`
- air around the mark — it should read as a seal, not a sticker
Marks are drawn as vector on the canvas (not rasterised SVG). **Awaiting the client's pick.**

## Services — settled
13 lines (see `PLAN.md`): commercial, office carpet, residential, apartment,
move in/out, post-construction, deep, one-time, school, church, sofa set,
toilet bowl & sink, **landscaping**.
**Fumigation is omitted everywhere — not licensed yet.** Revisit when the licence lands.
Source: `share_card.jpeg` (client-supplied 16/11/2026) + the company profile.

## Open
- Site build not started. Standard: zero-build static HTML/CSS/vanilla JS,
  .htaccess clean URLs + CSP, sitemap/robots, mobile sweep.
- Waiting on client: logo vector, job photographs, permission to name clients,
  testimonials, hours.
