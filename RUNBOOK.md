# Runbook — smartlinepointcleaning.co.ke

How to build, check, deploy and look after the site. Hosting is DirectAdmin
(`public_html`, Apache, PHP). Nothing on the server is built: you upload the
committed `site/` folder as a zip.

## 1. Build

```bash
python build_assets.py           # font, grain, shapes, QR, icons, logo, seal, images, share cards (needs: pip install segno)
# build_site.py also writes sitemap.xml (lastmod per page from build_cache/lastmod.json), robots.txt and the IndexNow key file
python build_assets.py --force   # re-encode every image, e.g. after changing a crop or the grade
python build_site.py             # 11 pages + .htaccess, PHP handler, sitemap, robots, manifest — verify() runs last
python make_upload.py            # dist/smartlinepointcleaning.co.ke-upload.zip, re-opened and checked
```

`build_site.py` refuses to write a broken site. It fails on: titles over 60
characters or descriptions outside 110–160, a missing canonical/OG/JSON-LD,
a broken internal link or `#anchor`, an image without `alt`/`width`/`height`,
inline script or style (the CSP forbids both), fumigation anywhere, JS over its
budget, a hero image over 200 KB.

Behaviour lives in `site/assets/js/main.js` (readable source); the build writes the
`main.min.js` that pages load, and the 30 KB JS budget is checked on that file.

Content lives in two files — edit these, never the HTML in `site/`:

| File | Holds |
|---|---|
| `site_layout.py` | Pages, sections, headings, service copy, SEO titles/descriptions, clients |
| `site_content.py` | Contact details, FAQ answers, compliance lines, privacy text, image crops, and the switches below |

### Switches in `site_content.py`

| Switch | Now | Change to |
|---|---|---|
| `LOGO_CONCEPT` | `"original"` — the client's own logo, lifted as vector from `smart.pdf` by `logo_original.py` | leave it; the round-2 concepts are superseded |
| `GA_ID` | `None` (no analytics, no cookie notice) | `"G-XXXXXXX"` — GA4 then loads only after the visitor accepts; CSP already allows it |
| `PRICES` | `None` (the pricing block explains how quotes work) | `{"visit": "4,500", "month": "18,000", "sqm": "45"}` shows "From KES …" |

## 2. Check before every upload

```bash
python serve_local.py 8765       # behaves like the live .htaccess: clean URLs, real 404 status
NODE_PATH=<dir>/node_modules node tools/qa_browser.cjs <out_dir>
```

`qa_browser.cjs` needs `puppeteer-core@23.11.1` installed in any folder
(`npm i puppeteer-core@23.11.1`) and drives the installed Chrome (or Edge if Chrome
is missing or will not start; set `QA_BROWSER` to force one). It loads all
11 pages at 1440 px and as a 390 px phone, fails on any console error, failed
request or sideways scroll, then clicks through the menu, mega menu, the
two-step quote form (validation and a real submit), the client filter, the
lightbox, and a pass with animations on. It must end `ALL CHECKS PASSED`.

Lighthouse on the local server (20/11/2026, v2 design): accessibility, best practices
and SEO **100** on all five pages tested, phone and desktop; performance 96–99 desktop,
83–94 phone, CLS ≤ 0.034. Observed LCP is ~210 ms; the simulated phone figure is held back
because the local server sends CSS/HTML/JS uncompressed — Apache's `mod_deflate` rule in
`.htaccess` cuts those about five-fold live. Re-run PageSpeed Insights after launch.

Motion is tested separately with animations on (loader, hero intro, statement scrub,
pinned services rail, steps): all must run with zero console errors.

## 2b. GitHub Pages preview — for showing the client before the domain is live

https://murayaallen.github.io/Smartline-Point-Cleaning-Hub-Ltd/ — published automatically: every push to `main` that touches `site/`
runs `.github/workflows/pages.yml`, which runs `make_pages.py` and force-pushes `dist/pages` to the
`gh-pages` branch (one commit, replaced each time). GitHub Pages serves that branch
(Settings → Pages → Deploy from a branch → `gh-pages` / root).

What `make_pages.py` changes, because Pages serves the repo under a sub-path and has no Apache/PHP:
every root path gets the `/Smartline-Point-Cleaning-Hub-Ltd/` prefix (HTML, srcset, CSS `url()`,
JS, manifest); every page is `noindex, nofollow` (canonical still points at the real domain);
og/twitter images point at the preview so WhatsApp shows the card; `.htaccess`, `form/`,
`robots.txt`, `sitemap.xml`, `.well-known/` and `speculation-rules.json` are left out; a valid
enquiry shows *"This is the preview link, so the form does not send yet"* instead of posting.
No CSP/HSTS headers and no hover prefetch there — those are `.htaccess` features of the live host.
`verify()` fails the build if any path escapes the prefix or points at a missing file.

Local check: `python make_pages.py`, serve `dist/pages` under `/Smartline-Point-Cleaning-Hub-Ltd/`
(extensionless → `.html`, unknown → `404.html`), browse every page on desktop and phone.

## 3. First deploy

1. **Domain.** Register `smartlinepointcleaning.co.ke`; point its nameservers at the host.
2. **Site in DirectAdmin.** Add the domain; issue Let's Encrypt for the apex **and** `www`.
   PHP 8.1 or later. `mod_rewrite`, `mod_headers`, `mod_deflate` on (they are by default).
3. **Upload.** File Manager → `public_html` → delete the host's placeholder `index.html`
   → upload the zip → extract in place. Confirm `.htaccess` and `form/.htaccess` arrived
   (dotfiles: turn on "show hidden" if the file manager hides them).
4. **Email.** Create `info@`, `accounts@`, `operations@`, `marketing@`, and **`website@`**
   (the form sends *from* this address, so it must exist for SPF/DKIM to pass).
   Turn on DKIM in DirectAdmin. DNS: SPF `v=spf1 a mx ~all` (or the host's include),
   DMARC `v=DMARC1; p=none; rua=mailto:info@smartlinepointcleaning.co.ke` to start.
5. **Form.** Submit a real enquiry from the live site, with your own email in it.
   Expect: the redirect to `/thank-you`, the enquiry in `info@`, the copy in your inbox
   (check spam on the first one). Six submissions inside an hour from one IP should be refused.

### Live checks — all must pass

| Request | Expect |
|---|---|
| `http://smartlinepointcleaning.co.ke/about` | one 301 to `https://smartlinepointcleaning.co.ke/about` |
| `https://www.smartlinepointcleaning.co.ke/` | one 301 to the apex |
| `/about.html`, `/index.html`, `/about/` | 301 to `/about`, `/`, `/about` |
| `/no-such-page` | the 404 page **with status 404** |
| `/.htaccess`, `/form/`, `/site_content.py` | 403 |
| `/form/enquiry.php` by GET | 303 to `/contact` |
| Response headers | CSP, HSTS, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Speculation-Rules` |
| `/speculation-rules.json` | 200, `application/speculationrules+json` (every other `.json` stays 403) |
| securityheaders.com | A or A+ |
| /contact map | The Google map loads at *Find us* (CSP `frame-src https://www.google.com`); no CSP error in the console |
| `/sitemap.xml` | 200, XML, 9 URLs, each with a `<lastmod>`; every URL opens with status 200 |
| `/robots.txt` | 200, `Allow: /`, `Disallow: /form/`, the `Sitemap:` line |
| `/4f82024d62e22d6a7fcff95721ad0647.txt` | 200, plain text, the key itself (IndexNow) |
| View source, any page | `<link rel="canonical">` = that page's apex URL; `index, follow` (thank-you and 404: `noindex`) |
| Rich Results Test, home + one service page | *Local business* and *Breadcrumbs* valid, no errors. FAQ will **not** show as a rich result: Google limits FAQ results to government and health sites since 2023, so FAQPage is valid markup only |
| validator.schema.org, home | the whole graph (LocalBusiness, WebSite, WebPage, FAQPage) with no errors |
| PageSpeed Insights, phone | 90+ performance, 100 the rest (local, compressed, 23/11/2026: phone 96–97, desktop 97–100, CLS 0) |
| A real phone | menu, form, WhatsApp button, tap-to-call |

## 4. Google and Bing, after launch (current practice, 23/11/2026)

Do these only after every live check in §3 passes. Accounts belong to the **client**
(sign in with a Google account they control, ideally `info@`); add Allen as a user.

**Business details — use exactly this everywhere (NAP consistency matters for local ranking):**
Smartline Point Cleaning Hub Ltd · ICIPE Road, Kasarani, Nairobi · +254 711 128736 ·
https://smartlinepointcleaning.co.ke · info@smartlinepointcleaning.co.ke

### 4.1 Google Search Console — day one
1. search.google.com/search-console → **Add property → Domain** → `smartlinepointcleaning.co.ke`.
   Google gives a TXT record (`google-site-verification=…`). Add it in DirectAdmin → DNS
   Management (host `@`), wait for it to resolve, press Verify. **Leave the TXT record in place
   for good** — removing it un-verifies the property. A Domain property covers http, https and www.
   - Fallback if DNS cannot be edited: add a *URL prefix* property, choose *HTML tag*, paste the
     `content` value into `site_content.GSC_VERIFY`, run `build_site.py`, upload `index.html`, Verify.
2. **Sitemaps** → submit `sitemap.xml`. Expect *Success* and 9 discovered pages.
3. **URL Inspection** → each of `/`, `/services`, `/commercial-cleaning`,
   `/residential-apartment-cleaning`, `/post-construction-cleaning`, `/about`, `/clients`, `/contact`
   → *Test live URL* (must say "URL is available to Google") → *Request indexing*.
   There is a daily quota (about 10); do the rest the next day.
4. **Settings → Users and permissions** — client as Owner, Allen as Full user.

### 4.2 Google Business Profile — the biggest lever for "cleaning company near me"
1. business.google.com → add the business, name exactly as above.
2. **Category:** primary *Commercial cleaning service*; additional *House cleaning service*,
   *Janitorial service*, *Carpet cleaning service*, *Upholstery cleaning service*, *Landscaper*.
   No fumigation/pest-control category (not licensed).
3. **Location:** show the office (ICIPE Road, Kasarani) **and** add service areas: Nairobi, Kasarani,
   Roysambu, Ruiru, Thika Road, Nairobi CBD, Westlands, Kiambu — the same list as the site's
   "Areas we serve" (max 20). Drop the pin on the real office — then send the
   pin's coordinates so `site_content.MAP_QUERY` and the schema can use the exact spot.
4. **Hours** (still to confirm with the client), **phone**, **website** = the apex URL,
   **WhatsApp** chat button with the same number.
5. **Services:** add all 13 from the site (names as on `/services`). **Description** (750 chars max):
   > Smartline Point Cleaning Hub Ltd is a Nairobi cleaning company, established in 2018 and based on
   > ICIPE Road, Kasarani. We clean offices, banks, schools, churches, homes, apartments and Airbnbs,
   > and handle post-construction, deep and one-time cleans, carpet and sofa cleaning, washrooms and
   > landscaping. Our cleaners are trained, uniformed and supervised; every job is scoped in writing,
   > and if anything is missed we come back within 24 hours to re-clean it. Daily, weekly, monthly or
   > one-off schedules across Nairobi and Kiambu. Call or WhatsApp +254 711 128736 for a free site
   > visit and a written quote.
6. **Verification:** Google usually asks for a short video (signage, office, equipment, proof of
   management). Plan it with the client.
7. **Photos:** REAL-07 — 10+ real photographs (team at work, equipment, finished jobs, office
   exterior). Stock photos get removed. Add a few new ones each month.
8. **Reviews:** after a job, send clients the profile's *Ask for reviews* link. Reply to every
   review. (The website deliberately carries no testimonials — reviews live on Google.)
9. When the profile is live, put its URL (and any social pages) into the schema `sameAs`
   (`build_site.business_node`), rebuild, upload.

### 4.3 Bing (also feeds ChatGPT search, Copilot and DuckDuckGo)
1. bing.com/webmasters → **Import from Google Search Console** (one click, no extra verification;
   fallback: `site_content.BING_VERIFY`).
2. `python tools/indexnow.py` (dry run) then `python tools/indexnow.py --send`. Re-run with `--send`
   after any later upload that changes pages; the sitemap `<lastmod>` dates move only for pages
   whose content changed.

### 4.4 Check-ins
- **Day 3–7:** Search Console → *Pages*: 9 indexed. *Not indexed* should list only `/thank-you`
  (noindex, by design) and redirect variants (http, www, `.html`) — those are correct.
  Search `site:smartlinepointcleaning.co.ke` on Google.
- **Week 4:** Search Console → *Performance* (queries, impressions), *Core Web Vitals* (appears once
  there is enough traffic), *HTTPS* (all pages HTTPS). Business Profile → *Performance* (calls,
  direction requests, website clicks).
- **Analytics** (optional): create a GA4 property, set `site_content.GA_ID`, rebuild, upload — the
  cookie notice and consent gate switch on with it.
- **The GitHub preview** (`murayaallen.github.io/…`) stays `noindex` with canonicals pointing at the
  real domain, so it never competes in search. It can be switched off after launch
  (repo Settings → Pages → Unpublish) once the client no longer needs the link.

## 5. Keeping it alive

- **Changing copy:** edit `site_layout.py` / `site_content.py` → `build_site.py` →
  QA → `make_upload.py` → upload the changed files (or the whole zip).
- **Swapping a stock photo for a real one:** point the key in `site_content.IMAGES`
  at the new file in `media/all/`, `build_assets.py --force`, `build_site.py`.
  Images are cached for 30 days, so a swap reaches returning visitors within a month
  (rename the key if it must be immediate).
- **Before/after sliders** and the **"The work"** gallery title switch on when
  REAL-03–06 arrive — see `MEDIA.md`.
- **`security.txt` expires 20/11/2027.** Rebuild and upload before then.
- **Renewal:** domain + server space KES 3,000 a year from year two.
- **Fumigation** stays off the site until the licence is in hand.
