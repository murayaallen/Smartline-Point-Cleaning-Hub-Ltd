# Runbook — smartlinepointcleaning.co.ke

How to build, check, deploy and look after the site. Hosting is DirectAdmin
(`public_html`, Apache, PHP). Nothing on the server is built: you upload the
committed `site/` folder as a zip.

## 1. Build

```bash
python build_assets.py           # font, grain, icons, logo, seal, images, share cards  (only when these change)
python build_assets.py --force   # re-encode every image, e.g. after changing a crop or the grade
python build_site.py             # 11 pages + .htaccess, PHP handler, sitemap, robots, manifest — verify() runs last
python make_upload.py            # dist/smartlinepointcleaning.co.ke-upload.zip, re-opened and checked
```

`build_site.py` refuses to write a broken site. It fails on: titles over 60
characters or descriptions outside 110–160, a missing canonical/OG/JSON-LD,
a broken internal link or `#anchor`, an image without `alt`/`width`/`height`,
inline script or style (the CSP forbids both), fumigation anywhere, JS over its
budget, a hero image over 200 KB.

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
| Rich Results Test, home + one service page | LocalBusiness, Breadcrumb, FAQ detected, no errors |
| PageSpeed Insights, phone | 90+ performance, 100 the rest |
| A real phone | menu, form, WhatsApp button, tap-to-call |

## 4. Google, after launch

1. **Search Console** — add a *Domain* property, verify by DNS TXT, submit
   `https://smartlinepointcleaning.co.ke/sitemap.xml`, request indexing for `/`,
   `/services` and the three service pages.
2. **Google Business Profile** — primary category *Commercial cleaning service*;
   add *House cleaning service*, *Janitorial service*, *Carpet cleaning service*,
   *Landscaper*. Name, address and phone **exactly** as in the site footer.
   Website = the apex URL. Needs **REAL-07**: 10+ real photographs (Google strips stock).
   Ask happy clients for reviews there — the site carries no testimonials by decision.
3. **Analytics** (optional) — create a GA4 property, set `GA_ID`, rebuild, upload.
4. Bing Webmaster Tools — import from Search Console in one click.

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
