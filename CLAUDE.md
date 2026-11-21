# Smartline Point Cleaning Hub Ltd — project notes

## Client
Smartline Point Cleaning Hub Ltd — commercial, residential, post-construction
cleaning and landscaping. Established 2018.
ICIPE Road, Sports Drive, Suite 8, Kasarani · P.O. Box 48018-00100, Nairobi
+254 711 128736 · their printed profile shows info@smartlineltd.co.ke — superseded: the site and
mailboxes use **@smartlinepointcleaning.co.ke** (see Domain below)
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
- `site_layout.py` — **single source of truth for the website layout**: every page, section,
  copy, SEO title/description, palette, type scale. `make_layout.py` renders it to
  `LAYOUT.md` (spec) and `wireframes.html` (clickable wireframe, desktop/mobile toggle,
  deep links like `wireframes.html#page=home&w=mobile`). `verify()` fails the build on
  titles > 60 chars, descriptions outside 110–160, contrast below AA, ≠ 8 pages,
  ≠ 13 services, or fumigation anywhere on the site. Edit the data, never LAYOUT.md.
- `brandkit.py` — shared ReportLab house style (palette, fonts, logo mark, masthead, footer).
- `make_choices.py` / `Smartline Point Cleaning Hub - Domain & Choices.pdf` — one-page
  tick-sheet sent to the client: 6 available domain names (recommendation flagged) plus
  client-naming, pricing-display and WhatsApp-number decisions. Ref AMM-D-2026-187.
  Note: run these scripts with plain `python`, not `python -I` (brandkit import).

## Status
Quote **accepted** (16/11/2026). **Website v2 BUILT and verified (20/11/2026)** — `site/`.
Next: client sign-offs in `CLIENT-REVIEW.md`, then deploy per `RUNBOOK.md`.

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

## Client brand colours — exact, read from the vectors in their profile PDF
Indigo S `#2F2483` (CMYK 100/100/0/0) · navy droplet `#101238` · swoosh gradient
`#FF6600 → #FFC200 (17%) → #F8951A (38%) → #FC621C`. Wordmark set in **Gotham Black**.
Tagline: *Assuring you the best*.

## Logo — the client's ORIGINAL logo is live (Allen, 20/11/2026: "use their original logo but high quality")
`logo_original.py` lifts it as **exact vector** from page 1 of `smart.pdf` — no tracing: it parses the
content stream for the S, droplet, gradient swoosh (stops + axis from the shading dictionary) and the
outlined tagline, and sets the wordmark from the profile's embedded Gotham Black subset (fontTools).
`verify()` on import. `python logo_original.py` writes the master set to `logo/original/`
(mark, full logo with tagline, two-line lock-up, each colour + reverse, PNG 512/1024).
`site_content.LOGO_CONCEPT = "original"`; the reverse version (white S + droplet, gradient kept)
is for navy. Header lock-up = S + SMARTLINE / POINT CLEANING HUB LTD in Gotham Black.
Rasters (favicons, share cards) are rendered from the profile page itself. The round-2 concepts
below are **superseded** — kept for the record, do not re-propose.

## Logo — round 2 concepts (superseded 20/11/2026)
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
Marks are drawn as vector on the canvas (not rasterised SVG). No longer awaiting a pick —
the client's own logo replaced them.

## Services — settled
13 lines (see `PLAN.md`): commercial, office carpet, residential, apartment,
move in/out, post-construction, deep, one-time, school, church, sofa set,
toilet bowl & sink, **landscaping**.
**Fumigation is omitted everywhere — not licensed yet.** Revisit when the licence lands.
Source: `share_card.jpeg` (client-supplied 16/11/2026) + the company profile.

## Website layout — SETTLED, build from this
`LAYOUT.md` + `wireframes.html`, generated from `site_layout.py`. 8 content pages (64 sections),
3 utility pages (thank-you, privacy, 404), 9 global elements incl. cookie notice (GA4 only after
consent). Home is 10 sections: hero → proof + trusted-by → welcome → services (+ schedules)
→ why → how we work → trained cleaners → guarantee → FAQ → CTA (testimonials removed 17/11/2026). Quote form is two
steps (the job, then you), six required fields, pre-filled from `?service=`.
- **Service copy for all 13 is DRAFT** — written by us, needs client approval. So do the
  one-line proofs under the six reasons (incl. the re-clean promise).
- Build standards (a11y, perf budget, SEO tech, security headers) and the image spec are in
  LAYOUT.md §4b–4c — that is the launch bar.

## Media — sourced online, by Allen's decision (17/11/2026)
`media_plan.py` is the source of truth → `MEDIA.md` (brief) + `Smartline - Image Sourcing List.xlsx`
(tracker). 29 stock images to source (21 P1), 6 reuses, 8 real-photo items only the client can
supply, 8 assets we produce. `verify()` fails if any image slot in site_layout.py has no media
planned, if a service row lacks its own photo, or if a brief mentions fumigation.
Wireframe notes now carry the image IDs (IMG-/REAL-) per section.
- Downloads go to `media/incoming/<folder>/` under the **Save as** name; client photos to
  `media/real/`. Both are **gitignored** — binaries stay out of the public repo.
- Rules that are not negotiable: stock is illustration, never evidence. No stock image is
  captioned as a Smartline job, team or client. No stock faces on testimonials. Before/after
  sliders stay hidden until REAL-03–05 arrive; the gallery runs as “Spaces we look after”
  until REAL-06 arrives. Google Business Profile needs REAL-07 — Google strips stock.
- Record source URL + photographer + licence for every approved image; the tracker flags
  any approved image with a blank licence.

## Images — COMPLETE, nothing is waiting (17/11/2026)
**Allen: do not wait for the real photographs.** Every slot is filled; `media_plan.missing()`
returns empty. 45 files in `media/all`: **29 placed, 9 gallery tiles, 7 dropped.**
- 19 new Pexels images downloaded at 2400px to close the last 12 gaps (team, About hero,
  supervisor, community, church, apartment linen, move in/out, sofa, homes hero,
  post-construction hero, hero alternate, BG-02). `review_media.py` holds the decision per file.
- `IMG-S10` upgraded from the scraped webp to `pexels-15798784.jpg` — same subject, licensed,
  three times the resolution. Provenance of placed images: 19 Pexels/Unsplash, 11 unknown
  (Allen's call, already settled).
- Only 3 of 30 are 1x-only, and each sits somewhere small (404 page, two gallery tiles).
- **Before/after sliders**: a stock pair would pass off another company's job as ours, so
  CC/RA/PC-05 ship as **“What finished looks like”** — photo + the written standard + the
  24-hour promise. The slider drops into the same slot when REAL-03–05 arrive. No layout change.
- **Gallery** ships now as “Spaces we look after” (true of stock); becomes “The work” when real
  job photos replace it.
- **Team photo caption stays generic** — “Trained, supervised teams”, never “our team”, while stock.
- Still genuinely blocked, and not by us: **REAL-07** (10+ real photos for Google Business
  Profile — Google strips stock). (Testimonials dropped and client naming granted — see below.)

## Client decisions — SETTLED 17/11/2026
- **No testimonials anywhere on the site.** Both testimonial sections removed (Home and
  Clients). Do not propose them again. The **named clients carry the proof instead** —
  stronger than a quote and impossible to fake.
- **Permission granted to name clients.** All nine publish: Jewel Complex, Uwezo Microfinance
  Bank, Richland Pointe, ACK St Paul's Mukuyuini, St Christopher's International School,
  Canon Kimani's House Airbnbs, Pataya Properties, Seven Point, Steph Underground Lounge.
  They appear in the Home proof strip, the Clients page and beside the contact form.
- Home 10 sections, Clients 5. Client logo files are an upgrade, not a blocker.

## Website build — DONE 20/11/2026
Pipeline: `build_assets.py [--force]` → `build_site.py` (verify gates) → `make_upload.py`
(zip in gitignored `dist/`) · preview `serve_local.py 8765` · QA `tools/qa_browser.cjs`
(puppeteer-core 23.11.1 + Chrome, falling back to Edge — Edge 158 refused to start headless on
21/11/2026 mid-update; `$QA_BROWSER` overrides; must end `ALL CHECKS PASSED`). Full steps in `RUNBOOK.md`.
- Content edits go in `site_layout.py` / `site_content.py`, never in `site/*.html` (generated).
  CSS/JS in `site/assets/` ARE hand-written source — edit them directly.
- Switches in `site_content.py`: `LOGO_CONCEPT="original"` (the client's logo),
  `GA_ID=None` (no analytics, no cookie bar), `PRICES=None` (pricing block explains quoting).
- Last verification (20/11/2026, v2): `verify()` OK (11 pages, JS 26.7 KB, fonts 67 KB, phone hero
  ≤ 200 KB, desktop hero ≤ 300 KB); browser QA all passed (11 pages × 1440/390 + menus, two-step
  form, filter, lightbox, loader, header hide/return, progress bar); motion-on check: loader, hero
  intro, statement scrub, pinned rail, steps all run with zero console errors; Lighthouse local:
  a11y/best-practices/SEO **100** on all 10 runs, perf 96–99 desktop, 83–94 phone (local server
  sends uncompressed; observed LCP 210 ms). 21/11/2026 width sweep: every page at 1920, 1280, 1024,
  768 and 360 — no overflow, no script errors.
- Schema is **LocalBusiness** (schema.org has no CleaningService type) — no geo, openingHours,
  sameAs or aggregateRating until the client supplies real values. The 404 page has no canonical.

## Website design v2 — "Clean Line" (Allen, 20/11/2026: v1 hero font "looks common for AI")
**Reversal, do not undo:** v1's Bodoni Moda + Manrope with an italic accent word, beige paper and
brass is gone — that serif-italic luxury look is the AI-template tell Allen named. v2 is built from
the client's own logo and from Allen's own sites (Vistex motion system, Viwanda kinetic type):
- **Type:** Mona Sans (OFL, self-hosted, one variable file wght 400–900 × wdth 100–125, 67 KB).
  Display wide and heavy (width 125%, weight 780–820, tight tracking) to sit beside their Gotham
  Black wordmark; body at normal width. Labels: wide caps with a gradient dash.
- **Colour:** navy/indigo from the logo, the swoosh gradient for primary buttons and accents,
  cool white/paper (`#F5F5FA`) for light sections. `--amber-ink #B04E08` for small amber text on
  white (plain amber fails contrast). Brass is retired.
- **Backgrounds** (systems, used with intent): *depth* on navy (two drifting glows, dot field,
  the S as a 4.5% watermark, film grain); *tiles* (fading tile grid) behind the welcome, approach
  and scope sections; *sun* warm wash behind the guarantee; photo washes in page heroes and CTA.
- **Motion** (`main.js`, one rAF loop, all off under reduced motion): loader where the S assembles
  (swoosh wipes, S rises, droplet drops) then a diagonal wipe; hero squeegee pass (fog clears behind
  a light blade), masked word rise, gradient pan; header goes solid, hides scrolling down, returns
  up, gradient progress line; headings split into masked words; the welcome statement lights word
  by word; parallax on hero/framed photos/band backgrounds; services rail **pinned and driven
  sideways by vertical scroll** on desktop (swipe deck on phones); How-we-work pinned scrollytelling
  with a big gradient step counter; diagonal wipe reveals on photos; drawn timelines; velocity
  marquees (client names, outlined CTA words); magnetic buttons + cursor glow on cards (mouse only);
  cross-page **view transitions** (Chromium). `boot.js` reveals everything if `main.js` never runs.
- **Prefetch on hover** (21/11/2026): `.htaccess` sends `Speculation-Rules: "/speculation-rules.json"`
  (a file, not inline script, so the CSP stays strict); Chromium prefetches same-site pages on hover
  (`eagerness: moderate`; `/form/*` and new-tab links excluded). Prefetch, **not prerender** — a
  prerendered page would play its hero intro unseen. `serve_local.py` sends the same header.
  Verified: hover fetched /about and /clients with `Sec-Purpose: prefetch`; clicks land in ~200 ms.
- Squeegee sheen: a diagonal light band wipes across card/gallery photos on hover.
- Keyboard: tabbing to an off-screen card in the pinned rail scrolls the page until it is in view.
- Icons: Lucide restyled, square caps, miter joins (Allen rejected rounded/childish icons) — now
  1.6px to match the heavier type, in tinted rounded tiles with a gradient dot.
- Home is full-bleed: art-directed hero (`hero-wide` 16:9 for laptops, `hero-tall` 9:16 for phones,
  same corridor photo) under a navy shade, glass stats strip, seal.
- **v3 (21/11/2026, Allen's brief):**
  - **No metrics anywhere.** Allen: "I dont want the fake metrics remove them." The hero stats strip
    (2018 / 9+ / 13 / 24h) is gone; QA fails if `[data-count]`/`.hstats` ever come back. Do not add
    counters, figures or "trusted by N" claims.
  - **Welcome** is kinetic: the client's statement splits into words that sharpen from blur, flash
    warm as they land and settle navy; key phrases (cleanliness meets excellence, spotless, fresh,
    healthier happier, satisfaction) carry the gradient with a drawn underline; the S outline draws
    itself in the margin with scroll; faded office photo in the white space.
  - **Interactive type:** on mouse devices the logo's colours follow the cursor through the hero
    headline, every display heading, the CTA title and the footer line (per-character colour, no
    layout shift); welcome words react the same way. Buttons and nav labels roll on hover.
  - **Why Smartline** is a **reasons index**, not cards: six large rows (accordion, `aria-expanded`),
    a sticky photo stage that wipes to each reason's photo, autoplay with a progress line on desktop
    (pauses on hover/focus), tap on phones. Photos per reason in `REASON_IMAGE` (build_site.py).
  - **White space carries photos and colour:** `bg_photo()` lays a faded, masked photo into light
    sections (welcome, guarantee, FAQ, About approach); `orbs()` drifts blurred sun/indigo colour
    (still on phones and under reduced motion).
  - **Every inner page hero has photos:** a background photo under the navy wash plus a framed photo.
    Two photos dropped only for being black-and-white are back as **navy duotones** (`duo-*-bg`,
    `_duotone()` in build_assets.py); two unused small shots frame heroes (`trolley`, `office-mop`).
    `verify()` now **fails if the same photo appears twice on one page**.
  - Phone performance: statement split, heading colour and text roll run at idle time; pointer-only
    effects are skipped on touch; blur off on phones; phone hero has a 760w step.
  - JS budget (≤ 30 KB, LAYOUT.md) is measured on what ships: `main.js` is the readable source,
    `build_site.py` writes `main.min.js` (comments/indent stripped) and pages load that.
- **v4 (21/11/2026):**
  - **"Wipe the glass"** (Allen: "the window wipe image can be used"): home section *The finish*
    between Training and the guarantee. `window cleaning.jpg` (key `wipe`) sits under a misted pane
    drawn on a canvas; the cursor (hover) or a finger (drag) clears it, a two-row demo pass runs on
    first view and yields the moment the visitor touches the glass, the button runs a full squeegee
    pass, "Streak-free" + sheen when ≥ 88 % is clear. `site/assets/js/wipe.js` → `wipe.min.js`
    (5 KB, own 8 KB budget), fetched by main.js only when the section is within 700 px; never under
    reduced motion (the photo is then simply clean). The home CTA band uses `duo-team-bg` because
    the window photo now leads its own section (no photo twice on a page).
  - **Training (home) is a training record**: one document card, six entries with icons, ticks that
    draw in sequence, "Before placement" stamp, supervisor sign-off line.
  - **Bug fixed — photos invisible with motion on:** Chrome counts `clip-path` when deciding
    visibility, so every `data-reveal="wipe"` photo (inner-page hero photos, About/service-page
    photos, home training) started fully clipped and never revealed. The reveal observer now
    watches the photo's parent, and a 300 ms safety net reveals anything already scrolled to (fast
    flings, anchor jumps, restored scroll). `qa_browser.cjs` now runs a **motion-ON sweep of every
    page on both devices** — the reduced-motion passes could not see this class of bug.
  - JS shipped is 29.5 KB of the 30 KB budget — new behaviour should go in an on-demand module
    like `wipe.js`, not into main.js.
- **v5 (21/11/2026) — no plain cards left on the inner pages:**
  - `training_record()` is shared: home Training and About Training both use the record card
    (About pairs it with the carpet-machine photo, `svc-carpet`).
  - Service pages: "What is included" is one **scope-of-work document** (`.record.scope`):
    groups flow in columns with drawn ticks, "Agreed in writing" stamp, supervisor sign-off and a
    link to get it scoped.
  - Clients: an **editorial index** — numbered rows, client names in large display type, a rule
    that extends and a warm wash on hover, sector chip; the filter and deep links are unchanged.
- **v6 (21/11/2026) — page loading screen, vector shapes, more on the inner pages:**
  - **Loading screen between pages** (Allen: "have a loading screen when switching across pages"):
    an internal link click wipes a navy panel in from the right (gradient squeegee edge, the client's
    S, a loading line), then navigates; `boot.js` sees the `sl-pt` flag and the next page paints
    covered, then the panel wipes off left. A valid form submit shows it while posting. Back/forward
    from bfcache clears it; a CSS-only exit fires at 2.6 s if JS never does; off under reduced
    motion. Cross-document view transitions were **removed** in favour of this (they snapshot it).
    The first-visit S-assembly loader is unchanged. QA checks leave + arrive + no stuck classes.
  - **Vector shapes** — original, generated by `build_assets.build_shapes()` from the logo's own
    geometry (`logo_original.part_path()`), so nothing to license: `waves` (wiped streaks along
    light-section edges), `drops` (the logo's droplet, faint, in inner heroes), `rings-light/dark`
    (seal rings behind inner heroes and the CTA phone number), `ribbon` (the swoosh echoed, on navy
    sections). Helpers: `shape()`, `waves()`, `bg_depth(ribbon=, hero=)`. Still under reduced motion.
  - **Services**: "Find your service — start with your premises": eight premises tabs (CSS-only
    radios, no JS) each showing a photo, a line and the services usually booked, with a quote link.
  - **Contact**: WhatsApp QR for desktop visitors (segno → `wa-qr.svg`, hidden on phones).
    `build_assets.py` now needs `pip install segno`.
  - **Privacy**: sticky "On this page" contents + "Ask about your data" link.
  - **Service pages**: a photo laid into the intro white space + streaks.
  - Mouse-only effects moved to **`fx.js`** (3.7 KB, loaded at idle on pointer devices only); main
    JS back to 27.7 KB. Gallery photos can share files with service photos (g-church = svc-church,
    g-linen = svc-apartment, g-newbuild = pc-hero) — the duplicate-photo guard catches it.
- QA note: images inside the phone swipe deck load when swiped to, so `qa_browser.cjs` skips
  `.rail__viewport` in its "never loaded" check — that is correct lazy behaviour, not a gap.
- CSP is strict (`script-src 'self'`, `style-src 'self'`): no inline scripts or style attributes;
  `verify()` fails on either. JSON-LD is the only inline script allowed.
- Images: one grade, focal-point crops, WebP 1x/1.5x/2x (hero adds 700w for phones). Cached
  30 days (filenames are not versioned); CSS/JS carry `?v=hash` and cache a year.
- The form posts to `/form/enquiry.php`, sending **from website@** — that mailbox must exist on
  the host. Honeypot, 3-second time trap, 5/hour per IP, customer copy.
- `security.txt` expires 20/11/2027 — rebuild before then.

## Open
- Client: sign-off on drafted copy (13 services, 20 FAQs, re-clean promise, standards,
  areas, privacy retention) — all listed in `CLIENT-REVIEW.md`. None blocks launch.
- Client supplies when ready: REAL-07 photos (GBP), REAL-03–06, hours, social handles,
  guide prices or none, map pin, GA4 yes/no.
- Deploy: register domain, DirectAdmin + SSL, upload zip, mailboxes incl. website@,
  SPF/DKIM/DMARC, live checks, Search Console, GBP — `RUNBOOK.md` §3–4.
