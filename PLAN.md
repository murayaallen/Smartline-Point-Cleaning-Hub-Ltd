# Smartline Point Cleaning Hub Ltd — website plan

Status: planning. Build not started. Quote AMM-Q-2026-187 accepted.

---

## 1. Domain

**CHOSEN BY THE CLIENT: `smartlinepointcleaning.co.ke`** (16/11/2026). Register this one.
It is the closest to the full registered company name; the client accepted the longer
string over the shorter alternatives. Everything below follows that choice — the existing
company profile prints `smartlineltd.co.ke`, so the profile reprint is now mandatory,
not optional, and it is already in the quoted scope.

Why this one:
- Their existing company profile already prints `smartlineltd.co.ke` **and**
  `info@smartlineltd.co.ke`. The profile is already circulating — the domain
  should match the paper, not the other way round.
- Matches the registered company name (Smartline Point Cleaning Hub **Ltd**)
  without carrying the full five-word name into the URL.
- Short enough to say on a phone call and to print on a van or an overall.

**`smartline.co.ke` is gone** — registered 07/04/2026 through KWE / Shujaahost by
another party, expires 07/04/2027. Not available and not worth chasing; never
print it.

Availability sweep (KENIC WHOIS, 16/11/2026):

| Domain | Status |
|---|---|
| smartlineltd.co.ke | **available — take this** |
| smartlinecleaning.co.ke | available (optional defensive buy) |
| smartlinecleaners.co.ke | available |
| smartlinepoint.co.ke | available |
| smartlinehub.co.ke | available |
| smartlinecleaninghub.co.ke | available |
| smartlinepointcleaning.co.ke | available |
| smartlineservices.co.ke | available |
| smartline.co.ke | **taken** (other company, exp. 07/04/2027) |

Worth raising once, now that the long name is chosen: `smartlineltd.co.ke` at KES 2,000/yr
as a 301 redirect, because that is the name already printed on their profile and the one
anyone holding the old paper will type. Not in the quoted price.

**Canonical form:** `https://smartlinepointcleaning.co.ke` (apex) as canonical;
`www.smartlinepointcleaning.co.ke` 301s to apex; all `http://` 301s to `https://`.
One canonical host only — never let both resolve 200.

## 2. Email

Included in the hosting line, created at setup:

| Mailbox | Use |
|---|---|
| info@ | public address on the site, profile and Google |
| accounts@ | invoices, M-Pesa confirmations, KRA |
| operations@ | job scheduling, supervisors |
| marketing@ | social, quotes follow-up |

Add on request at no cost: `sales@`, `hr@`, `careers@`, `quotes@`.

Technical: catch-all **off** (spam magnet), SPF, DKIM and a DMARC record at
`p=quarantine` so mail from the new domain is not junked. Webmail link plus
IMAP settings written into the handover sheet.

## 3. Sitemap — 8 pages

| # | Page | Purpose / primary search intent |
|---|---|---|
| 1 | `/` Home | Who they are, what they clean, request a quote |
| 2 | `/about` | Since 2018, training, culture-fit, CSR and job creation |
| 3 | `/services` | Hub — all thirteen service lines with anchors |
| 4 | `/commercial-cleaning` | "office cleaning services Nairobi" |
| 5 | `/residential-airbnb-cleaning` | "apartment / Airbnb cleaning Nairobi" |
| 6 | `/post-construction-cleaning` | "post construction cleaning Nairobi" |
| 7 | `/clients` | Jewel Complex, Uwezo Microfinance Bank, Richland Pointe, ACK St Pauls Mukuyuini, St Christopher's International School, Pataya, Seven Point, Steph Underground Lounge |
| 8 | `/contact` | Quote form → info@, WhatsApp, map, hours |

The remaining service lines live as sections inside `/services` — enough for
search, without thinning the site into stub pages.

### Services — final list (from the share card supplied 16/11/2026)

1. Commercial cleaning
2. Office carpet cleaning
3. Residential cleaning
4. Apartment cleaning
5. Move in / move out cleaning
6. Post-construction cleaning
7. Deep cleaning
8. One-time cleaning
9. School cleaning
10. Church cleaning
11. Sofa set & upholstery cleaning
12. Toilet bowl & sink cleaning *(from the company profile)*
13. **Landscaping** *(from the company profile — carried onto the site)*

**Fumigation is omitted.** The share card lists it, but the company is not
licensed for it yet. It stays off the website, the profile and the social posts
until the licence is in hand — advertising it unlicensed is a liability in a
tender. Add it as a service page the week the licence lands.

### Lines taken from the share card (client's own words)

- Positioning: *“We provide high quality cleaning services designed to keep your
  spaces spotless.”*
- Tagline: *“Assuring you the best”*
- Seal: *“Clean Quality Guaranteed”*
- Call to action: *“Book your clean today”* → +254 711 128736
- Why choose us: flexible scheduling · qualified cleaners · trustworthy and
  friendly · affordable · keen on details · quality results

Source file: `share_card.jpeg`.

### Home, section by section
1. Hero — "Assuring you the best", one line on what they do, two buttons:
   *Request a quote* and *WhatsApp us*.
2. Trust bar — since 2018 · trained and groomed staff · 9+ sites served ·
   comprehensive, quarterly, semi-annual or annual contracts.
3. Services grid — six cards, each linking into the hub or its own page.
4. Why Smartline — the training list from their profile (communication,
   equipment use, chemical handling, grooming and PPE, teamwork, code of conduct).
5. How it works — site visit → scope and quote → trained team assigned →
   supervised delivery → review.
6. Clients served — named, with permission.
7. Quote CTA band.
8. FAQ — five questions, marked up as FAQPage.
9. Footer — full NAP, hours, service areas, email, WhatsApp.

## 4. Design direction

Taken from their own profile and logo, not invented:

| Token | Value | Use |
|---|---|---|
| Navy | `#121439` | headers, footers, body text |
| Indigo | `#2E2482` | brand blocks, links, section fills |
| Orange | `#F98719` | CTA buttons, accents, underlines |
| Paper | `#FFFFFF` / `#F6F7FB` | backgrounds, alternating bands |

Photography-led (clean floors, kitchens, post-construction before/after),
generous white space, real shadow and depth on cards, no flat bootstrap tiles.
Type: one strong grotesque for headings, same family at lighter weight for body.
`prefers-reduced-motion` honoured; WCAG AA contrast on every pairing —
orange on white needs `#C96A0B` for text-size use, orange stays for fills.

## 5. Build

Zero-build static site: hand-written HTML5, CSS3, vanilla JS. No framework, no
npm, no compile step — the folder uploads straight to `public_html`.

```
site/
  index.html
  about/ services/ commercial-cleaning/ ... (folder-per-page, clean URLs)
  assets/css/   style.css
  assets/js/    main.js
  assets/img/   *.webp (+ .jpg fallback)
  assets/doc/   smartline-company-profile.pdf
  form/         enquiry.php      (honeypot + time-trap + rate limit → info@)
  .htaccess     https, www→apex, clean URLs, CSP, HSTS, gzip, cache headers
  sitemap.xml   robots.txt       site.webmanifest  favicons
```

Performance and SEO targets: Lighthouse ≥ 95 mobile, LCP < 2.0s on 4G,
WebP + `loading="lazy"` + explicit width/height on every image,
`CleaningService` schema with `areaServed` Nairobi + Kiambu, `Service` schema per
service page, `FAQPage` on home, `BreadcrumbList` on inner pages.

Google: Business Profile created and verified (category *Commercial cleaning
service*, service areas, hours, photos), Search Console verified via DNS TXT,
sitemap submitted, GA4 connected, quote-form submission tracked as a conversion.

## 6. Social launch pack

Six designed posts, client colours, delivered as 1080×1080 and 1080×1350 plus a
1080×1920 WhatsApp status and a 1200×627 LinkedIn card:
1. "We are live" — the new site
2. Services carousel
3. Post-construction before/after
4. Trained staff / PPE and grooming
5. Clients served
6. "Get a quote in 24 hours" — direct to the contact page

## 7. What we need from the client (blocks the build)

- Logo as vector (AI/EPS/SVG) or the largest PNG they hold
- 15–25 photographs of actual jobs, including before/after sets
- Team photo and two or three staff-at-work shots
- Written permission to name the clients listed in the profile
- Working hours, emergency/weekend policy, payment terms
- Any certificates, insurance cover or NEMA/KEBS documents to show
- Three to five client testimonials with names and titles
- Confirmation of the physical address and the WhatsApp number (+254 711 128736)

## 8. Timeline — 14 to 21 days from deposit

| Days | Work |
|---|---|
| 1 | Deposit received. Domain registered, hosting opened, mailboxes live, SPF/DKIM/DMARC set |
| 2–4 | Content gathering, copywriting, photo editing and WebP conversion |
| 5–9 | Build: home, then inner pages; form and `.htaccess` |
| 10–12 | Client review round and corrections |
| 13–15 | SEO, schema, Google Business Profile, Search Console, GA4, performance pass |
| 16–18 | Company profile redesign + social launch pack |
| 19–21 | Mobile sweep, launch, handover of every account, training. Balance due |

## 9. Open decisions

- [ ] Client confirms `smartlineltd.co.ke` (and whether to add the defensive name)
- [ ] Permission to publish the client list
- [ ] Do they want prices or price ranges shown, or quote-on-request only
- [ ] Preferred WhatsApp number for the site button — company line or operations
