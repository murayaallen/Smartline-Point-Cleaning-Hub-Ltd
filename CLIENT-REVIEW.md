# Client sign-off — before go-live

The site is built and every page is populated. These are the lines we wrote on
the client's behalf, or that wait on something only the client has. None of
them blocks launch except where marked; each is a one-line change in
`site_content.py` or `site_layout.py`, then rebuild.

## Approve or correct (we drafted these)

| # | Item | Where it shows | Source |
|---|---|---|---|
| 1 | **Logo** — their own logo, rebuilt as sharp vector from the company profile (S, swoosh, droplet, tagline; name in their Gotham Black). Confirm they are happy with the two-line header lock-up | header, footer, loader, seal, favicon, share cards | `logo_original.py` |
| 2 | **13 service descriptions** — one-line and long versions | Home, Services, the three service pages | `site_layout.SERVICE_COPY` |
| 3 | **"Clean Quality Guaranteed — 24-hour re-clean"** — a promise the business must keep | Home, service pages, footer badge | `GUARANTEE_SHORT` |
| 4 | **Six reasons and their one-line proofs** — "the same supervised team on your site", "no surprise charges" are commitments | Home "Why Smartline" | `site_layout.WHY` |
| 5 | **20 FAQ answers** — written conservatively: no prices, no fixed times, site visit "before any cost is involved", reply "within one working day" | every page's FAQ | `FAQ` |
| 6 | **Standards list** — training before placement, named supervisor, uniforms, chemicals at the right dilution, waste segregated, company registration + KRA PIN for procurement | About, Commercial | `COMPLIANCE` |
| 7 | **Areas served** — Nairobi and Kiambu | footer, schema, FAQ | `AREAS` |
| 8 | **Privacy notice** — enquiries deleted within 12 months; client records kept for the contract plus the legal period | /privacy | `PRIVACY` |
| 9 | **Named clients** — all nine, permission given 17/11/2026 | Home proof strip, Clients, Contact | `site_layout.CLIENTS` |
| 10 | **"The finish" copy** — "Glass shows every shortcut… see the standard we work to on every visit" (a stock photo of a window washer is the interactive; it is not presented as their job) | Home, "Clean you can see through" | `build_site.home()` |
| 11 | **Training record** — "Before placement" and "Refreshed on the job by a named supervisor" are commitments | Home, Training | `build_site.home()` |

## Supply (we cannot invent these)

| # | Item | What it unlocks | Blocks launch? |
|---|---|---|---|
| 10 | **10+ real photographs** of jobs and team (REAL-07) | Google Business Profile — Google strips stock | No — blocks the GBP, not the site |
| 11 | Before/after pairs of real jobs (REAL-03–05) | the before/after sliders replace "What finished looks like" | No |
| 12 | Real job photos for the gallery (REAL-06) | "Spaces we look after" becomes "The work" | No |
| 13 | **Working hours** | schema `openingHours`, GBP, contact page | No — omitted, never guessed |
| 14 | **Social media handles** (Facebook, Instagram, LinkedIn) | footer links, schema `sameAs`, launch posts | No |
| 15 | **Guide prices** — three "from" figures, or a decision to show none | pricing block on Services (`PRICES`) | No — the block explains how quotes work |
| 16 | Client logo files | logo strip instead of names | No |
| 17 | Exact map pin | schema `geo`, map link | No |
| 18 | GA4 — whether they want analytics | `GA_ID`; cookie notice appears only then | No |

## Settled — do not reopen

No testimonials anywhere · fumigation omitted until licensed · stock images are
never captioned as Smartline's own work, team or clients · domain
`smartlinepointcleaning.co.ke`.
