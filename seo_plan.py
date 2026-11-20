# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — SEO plan, single source of truth.

    python seo_plan.py   ->  SEO.md

Tied to site_layout.py, so the keyword map can never drift from the pages that
exist. verify() fails on: a page with no primary keyword, a primary keyword used
on two pages (cannibalisation), a keyword missing from its own title or H1, a
title over 60 characters, a description outside 110-160, a service with no target
term, or a page with no internal links planned.

Volumes are not guessed here. Kenya volumes are thin in every public tool; the
honest method is to ship, then read Search Console after 30 days and write the
real numbers into this file.
"""
from collections import Counter, OrderedDict

import site_layout as L

DOMAIN = "smartlinepointcleaning.co.ke"
BRAND = "Smartline Point Cleaning Hub Ltd"
PHONE_E164 = "+254711128736"
GEO = ("-1.2195", "36.8968")          # ICIPE Road, Kasarani — refine from the GBP pin

# ---------------------------------------------------------------- keyword map
# slug -> (primary, [secondary], [long tail], intent, note)
KEYWORDS = {
    "/": ("cleaning services in Nairobi",
          ["cleaning company Nairobi", "professional cleaning services Kenya",
           "commercial and residential cleaning Nairobi"],
          ["best cleaning company in Nairobi", "cleaning services near me Nairobi",
           "trusted cleaning company Kasarani"],
          "Commercial + navigational",
          "The hardest term and the slowest to move. The home page carries it, but the "
          "service pages are what will actually rank first."),
    "/about": ("professional cleaning company Nairobi",
               ["vetted cleaners Nairobi", "trained cleaning staff Kenya", "cleaning company since 2018"],
               ["are cleaning companies in Nairobi insured", "vetted cleaners for offices Nairobi"],
               "Trust / consideration",
               "Ranks for the questions buyers ask before shortlisting. The vetting table (A-06) is the "
               "content that earns this."),
    "/services": ("cleaning services Nairobi prices",
                  ["office cleaning cost Nairobi", "cleaning services price list Kenya",
                   "cleaning company packages Nairobi"],
                  ["how much does office cleaning cost in Nairobi",
                   "cleaning services price per square metre Kenya"],
                  "Commercial investigation",
                  "Cost queries are where the competitors actually win traffic. The guide-price block "
                  "(S-07) is what makes this page eligible for them \u2014 with no figures it cannot rank for cost."),
    "/commercial-cleaning": ("commercial cleaning Nairobi",
                             ["office cleaning services Nairobi", "janitorial services Nairobi",
                              "contract cleaning Nairobi"],
                             ["office cleaning services in Westlands", "daily office cleaning contract Nairobi",
                              "bank and school cleaning services Nairobi"],
                             "High-intent commercial",
                             "The highest-value page on the site. One contract repays the whole build."),
    "/residential-apartment-cleaning": ("house cleaning services Nairobi",
                                        ["apartment cleaning Nairobi", "Airbnb cleaning Nairobi",
                                         "home cleaning services Kenya"],
                                        ["Airbnb turnover cleaning Nairobi", "apartment deep cleaning Kilimani",
                                         "house cleaning services Kasarani"],
                                        "High-intent consumer",
                                        "Fastest to rank and fastest to convert \u2014 households decide in one visit, "
                                        "usually on a phone."),
    "/post-construction-cleaning": ("post construction cleaning Nairobi",
                                    ["builders cleaning services Nairobi", "after construction cleaning Kenya",
                                     "handover cleaning Nairobi"],
                                    ["post construction cleaning cost Nairobi",
                                     "cleaning after renovation Nairobi"],
                                    "Niche, high-value, low competition",
                                    "Least contested of the three service pages. Likely the first page to reach "
                                    "the top of the results."),
    "/clients": ("cleaning company clients Nairobi",
                 ["commercial cleaning references Kenya", "cleaning company portfolio Nairobi"],
                 ["which companies use professional cleaners in Nairobi"],
                 "Trust / proof",
                 "Rarely a landing page. It exists to convert people who arrived elsewhere, and to "
                 "carry the sector terms."),
    "/contact": ("cleaning services quote Nairobi",
                 ["book cleaning services Nairobi", "cleaning company contact Nairobi"],
                 ["get a cleaning quote in Nairobi", "book a cleaner today Nairobi"],
                 "Transactional",
                 "Also the page Google surfaces for brand searches. Keep the NAP identical to the GBP."),
}

# service -> the term its row and quote link should target (13 of them)
SERVICE_TERMS = {
    "Commercial cleaning": "commercial cleaning Nairobi",
    "Office carpet cleaning": "office carpet cleaning Nairobi",
    "School cleaning": "school cleaning services Nairobi",
    "Church cleaning": "church cleaning services Nairobi",
    "Residential cleaning": "house cleaning services Nairobi",
    "Apartment cleaning": "apartment cleaning Nairobi",
    "Move in / move out cleaning": "move out cleaning services Nairobi",
    "Sofa set & upholstery cleaning": "sofa set cleaning Nairobi",
    "Toilet bowl & sink cleaning": "washroom cleaning services Nairobi",
    "Post-construction cleaning": "post construction cleaning Nairobi",
    "Deep cleaning": "deep cleaning services Nairobi",
    "One-time cleaning": "one time cleaning Nairobi",
    "Landscaping": "landscaping services Nairobi",
}

# page -> pages it must link to (internal linking is the cheapest ranking lever we control)
INTERNAL = {
    "/": ["/services", "/commercial-cleaning", "/residential-apartment-cleaning",
          "/post-construction-cleaning", "/about", "/clients", "/contact"],
    "/about": ["/services", "/clients", "/contact"],
    "/services": ["/commercial-cleaning", "/residential-apartment-cleaning",
                  "/post-construction-cleaning", "/clients", "/contact"],
    "/commercial-cleaning": ["/services", "/clients", "/contact", "/residential-apartment-cleaning"],
    "/residential-apartment-cleaning": ["/services", "/clients", "/contact", "/post-construction-cleaning"],
    "/post-construction-cleaning": ["/services", "/clients", "/contact", "/commercial-cleaning"],
    "/clients": ["/services", "/commercial-cleaning", "/contact"],
    "/contact": ["/services", "/about"],
}

ONPAGE_RULES = [
    ("Title", "`Primary keyword | Smartline` under 60 characters. The keyword leads, the brand closes. "
              "Never two pages with the same title."),
    ("Meta description", "110\u2013160 characters, written to be clicked, not to be read by a crawler. "
                         "Include the primary term once, a reason to choose (trained, supervised, since 2018) "
                         "and an action (request a quote)."),
    ("H1", "One per page, carrying the primary keyword in natural language. The home page H1 is the "
           "client's own line \u2014 *Where cleanliness meets excellence* \u2014 with the keyword in the sub-line "
           "immediately under it."),
    ("H2 / H3", "Section headings carry the secondary and long-tail terms: *What is included*, *How it runs*, "
                "*What it costs*, *Questions*. Write for a reader; the terms fit naturally because they are "
                "what people ask."),
    ("First 100 words", "Say what the service is, where it is offered and who it is for, in plain words, "
                        "above the fold. Both the crawler and the visitor decide here."),
    ("URLs", "Lower case, hyphenated, no dates, no stop words: `/commercial-cleaning`, not "
             "`/our-services/commercial-cleaning-services-in-nairobi`. No trailing slash, no `.html`."),
    ("Images", "Descriptive file names (`office-cleaning-nairobi.webp`, not `IMG-S01.webp`) and alt text "
               "written per image. Alt describes the picture, it is not a keyword dump."),
    ("Internal links", "Every service page links back to the hub, to two related services and to the quote "
                       "form, with descriptive anchor text \u2014 *post-construction cleaning*, never *click here*."),
    ("Content length", "Service pages 600\u2013900 words of real substance (scope, method, FAQs). The home page "
                       "shorter. Nothing padded: thin or repetitive pages are what makes the competitors' "
                       "SEO pages worthless."),
]

SCHEMA = [
    ("Every page", "`Organization` + `BreadcrumbList`", "Name, logo, url, sameAs (the social profiles)."),
    ("Home", "`LocalBusiness` (schema.org has no CleaningService type) + `WebSite` + `FAQPage`",
     "address, geo, telephone, email, openingHours, areaServed (Nairobi, Kiambu), priceRange, image, "
     "hasOfferCatalog listing all 13 services."),
    ("Service pages", "`Service` + `FAQPage`",
     "serviceType, provider (@id of the LocalBusiness node), areaServed, hasOfferCatalog of what is included."),
    ("Services hub", "`CollectionPage` + `OfferCatalog`", "All 13 services as `Offer` items with names and urls."),
    ("Clients", "`CollectionPage`", "No fake `Review` or `aggregateRating` markup \u2014 see the warning below."),
    ("Contact", "`ContactPage` + the `LocalBusiness` node", "Identical NAP to the GBP, character for character."),
    ("Thank you / 404", "none", "`noindex, follow`."),
]

TECH = [
    ("Canonical", "Self-referencing canonical on every page: `https://smartlinepointcleaning.co.ke/path`, "
                  "apex host, https, no trailing slash, no index.html. One host answers 200 \u2014 everything "
                  "else 301s."),
    ("Redirects", "`http \u2192 https`, `www \u2192 apex`, `/index.html \u2192 /`, trailing slash stripped. All single-hop "
                  "301s: chains leak the little authority a new domain has."),
    ("sitemap.xml", "Only the 9 indexable URLs (8 content + /privacy), each with a real `lastmod`. "
                    "Regenerated by the build, submitted in Search Console."),
    ("robots.txt", "Allow everything, point at the sitemap, disallow `/form/`. No blanket blocks."),
    ("Core Web Vitals", "LCP < 2.0s on 4G, CLS < 0.05, INP < 200ms. On a Kenyan mobile connection this is a "
                        "ranking factor you can feel: WebP with srcset, explicit width and height, two WOFF2 "
                        "subsets preloaded, no framework, under 30 KB of JavaScript."),
    ("Mobile", "Mobile-first indexing means the phone layout *is* the indexed page. Same content on both \u2014 "
               "nothing hidden behind `display:none` on mobile."),
    ("HTTPS and headers", "HSTS, CSP, X-Content-Type-Options, Referrer-Policy. Mixed content breaks the "
                          "padlock and the trust signal with it."),
    ("Analytics", "GA4 after consent; `generate_lead`, `click_call`, `click_whatsapp`, `file_download` as "
                  "conversions. Search Console verified by DNS TXT so it survives a host change."),
    ("Bing", "Bing Webmaster Tools, import from Search Console. Five minutes, and it feeds Copilot answers."),
]

GBP = [
    ("Primary category", "**Commercial cleaning service**. The single heaviest lever in the local pack \u2014 "
                         "get this one right before anything else."),
    ("Secondary categories", "House cleaning service \u00b7 Carpet cleaning service \u00b7 Janitorial service \u00b7 "
                             "Landscaper. No more than fits the truth."),
    ("Business model", "Service-area business covering Nairobi County and Kiambu. The Kasarani address stays "
                       "on file for verification but the service area is what is published."),
    ("NAP", "Name, address and phone identical to the website footer, the contact page schema and the reprinted "
            "company profile. One character of difference is one more entity for Google to disambiguate."),
    ("Services", "All 13 loaded as GBP services, each with the same description used on the site."),
    ("Photos", "`REAL-07` \u2014 at least ten genuine photographs: logo, cover, premises, team, and five at work. "
               "Google removes stock images from profiles, so none of the sourced set can be used here."),
    ("Posts", "One a fortnight: a finished job, a service, a seasonal note (long rains \u2192 post-storm deep cleans). "
              "Posts are cheap and they keep the profile active."),
    ("Q&A", "Seed the eight real questions from the site FAQ and answer them from the business account."),
    ("Reviews", "The second heaviest lever, and the one nobody does properly. Ask at handover, every time: a QR "
                "card in the supervisor's folder and a WhatsApp link after the final visit. Reply to every "
                "review within 48 hours, including the bad ones. **Never buy or fabricate a review** \u2014 and "
                "never mark up an `aggregateRating` that is not real."),
    ("UTM", "Tag the GBP website link `?utm_source=gbp&utm_medium=organic` so the profile's traffic is "
            "separable in GA4."),
]

CITATIONS = [
    ("Google Business Profile", "The one that matters", "Launch week"),
    ("Bing Places", "Imports from GBP", "Launch week"),
    ("Facebook + Instagram business profiles", "NAP consistency, and where Kenyan clients check you are real",
     "Launch week"),
    ("LinkedIn company page", "Facility managers and procurement look here", "Launch week"),
    ("Jiji Kenya, Yellow Pages Kenya, BusinessList.co.ke, Kenyaplex", "Free local citations; same NAP each time",
     "Month 1"),
    ("Nairobi apartment and estate groups (WhatsApp, Facebook)", "Where Airbnb and residential work actually "
     "comes from in Nairobi \u2014 not a link, but a referral channel worth more than most directories", "Ongoing"),
]

CONTENT = [
    ("What office cleaning costs in Nairobi, honestly",
     "The competitors' cost pages are thin and contradictory \u2014 KES 15 to 80 per m\u00b2 for the same work. "
     "One honest, sourced page explaining what drives the price would outrank all of them and feeds every "
     "quote conversation.", "Phase 2"),
    ("A checklist: what to ask a cleaning company before you sign",
     "Vetting, insurance, statutory compliance, supervision, what happens when a cleaner is absent. Smartline "
     "answers all five; most competitors answer none. The page sells itself.", "Phase 2"),
    ("Area pages \u2014 Kasarani, Ruiru, Roysambu, Westlands, CBD",
     "One blanket areas page does not rank; a page each does. Real local content, not the same text with the "
     "place name swapped \u2014 that is what gets them filtered out.", "Phase 2"),
    ("Post-construction handover guide for contractors",
     "Targets the lowest-competition, highest-value term on the site, aimed at a buyer who repeats.", "Phase 3"),
]

RISKS = [
    ("Fabricated proof", "No invented statistics, no bought reviews, no `aggregateRating` markup without real "
                         "reviews behind it. Google has manual actions for review spam, and a Nairobi client who "
                         "spots a fake number tells other clients."),
    ("Duplicate or scraped copy", "Every word on this site is written for it. The competitors' duplicated "
                                  "directory pages are exactly why they rank badly for anything competitive."),
    ("Keyword stuffing", "'Cleaning services Nairobi' eleven times in a paragraph reads as desperate to a "
                         "human and adds nothing for a crawler."),
    ("Thin area pages", "Five near-identical pages with a place name swapped will be filtered. Write them "
                        "properly or not at all."),
    ("NAP drift", "The printed profile still shows the old domain and the old address format. Reprint it, and "
                  "fix every profile at once \u2014 a mismatch between citations is a ranking tax."),
    ("Expecting speed", "A new domain on competitive head terms takes months. The service pages and the local "
                        "pack move first; `cleaning services in Nairobi` is a year-one goal, not a month-one one."),
]

MEASURE = [
    ("Week 1", "Search Console and Bing verified, sitemap submitted, GBP live and verified, all 9 URLs indexed "
               "(check with `site:` and the URL Inspection tool)."),
    ("Day 30", "Baseline recorded: impressions, clicks, average position per page; GBP views, calls, direction "
               "requests. This is the first honest keyword data for Kenya \u2014 write the real terms back into "
               "this file."),
    ("Day 60", "Service pages ranking for their own names; post-construction and the long-tail terms on page 1 "
               "or 2. First reviews in. Quote-form conversions tracked in GA4."),
    ("Day 90", "Local pack presence for at least one core term in Kasarani/Ruiru. Decide phase 2 (area pages, "
               "cost guide) from what Search Console actually shows, not from this plan."),
    ("Monthly", "30 minutes: Search Console queries and pages, GBP insights, any 404s or crawl errors, "
                "Core Web Vitals report. Add the FAQ answers people actually searched for."),
]


# ================================================================== checks
def pages():
    return {pg["slug"]: pg for pg in L.PAGES}


def verify():
    errs = []
    pg = pages()
    for slug in pg:
        if slug not in KEYWORDS:
            errs.append("no keyword map for %s" % slug)
    for slug in KEYWORDS:
        if slug not in pg:
            errs.append("keyword map for a page that does not exist: %s" % slug)
    prim = [v[0].lower() for v in KEYWORDS.values()]
    for k, n in Counter(prim).items():
        if n > 1:
            errs.append("keyword cannibalisation \u2014 '%s' is primary on %d pages" % (k, n))
    for slug, (p, sec, tail, intent, note) in KEYWORDS.items():
        if slug not in pg:
            continue
        page = pg[slug]
        head = (page["title"] + " " + page["h1"] + " " + page["sections"][0]["p"].get("sub", "")).lower()
        sig = [w for w in p.lower().split() if len(w) > 4]
        hit = [w for w in sig if w in head]
        if len(hit) < max(2, int(len(sig) * 0.6)):
            errs.append("%s: primary keyword '%s' barely present in title/H1/hero (%d of %d words)"
                        % (slug, p, len(hit), len(sig)))
        if len(page["title"]) > 60:
            errs.append("%s: title over 60 chars" % slug)
        if not 110 <= len(page["desc"]) <= 160:
            errs.append("%s: description outside 110-160" % slug)
        if not sec or not tail:
            errs.append("%s: needs secondary and long-tail terms" % slug)
    services = [s for _, _, items in L.GROUPS for s, _ in items]
    for s in services:
        if s not in SERVICE_TERMS:
            errs.append("no target term for service: %s" % s)
    for extra in set(SERVICE_TERMS) - set(services):
        errs.append("target term for a service that is not on the site: %s" % extra)
    for slug, links in INTERNAL.items():
        if slug not in pg:
            errs.append("internal links from a page that does not exist: %s" % slug)
        for t in links:
            if t not in pg:
                errs.append("%s links to a page that does not exist: %s" % (slug, t))
        if "/contact" not in links and slug != "/contact":
            errs.append("%s does not link to the quote form" % slug)
    if errs:
        raise SystemExit("SEO verify() FAILED:\n  - " + "\n  - ".join(errs))
    return len(KEYWORDS), len(SERVICE_TERMS)


# ================================================================== SEO.md
def table(rows, head):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)


def build_md():
    n_pages, n_services = verify()
    pg = pages()
    o = ["# SEO plan — %s\n" % DOMAIN,
         "Generated from `seo_plan.py`, which reads `site_layout.py`. Edit the data and rebuild; "
         "`verify()` refuses to write this file if a page has no keyword, two pages fight over the same "
         "one, or a keyword is missing from its own title and H1.\n",
         "The order of work is deliberate: **technical foundation → on-page → Google Business Profile → "
         "reviews → content**. Most cleaning companies in Nairobi do the last one first and wonder why "
         "nothing moves.\n",
         "## 1. Keyword map\n",
         "No volume figures here. Kenyan volumes in public tools are unreliable, and we will have real "
         "numbers from Search Console 30 days after launch — those get written back into this file.\n"]
    rows = []
    for slug, (p, sec, tail, intent, note) in KEYWORDS.items():
        rows.append((("`%s`" % slug), "**%s**" % p, " · ".join(sec), " · ".join(tail), intent))
    o.append(table(rows, ["Page", "Primary", "Secondary", "Long tail", "Intent"]))
    o.append("")
    for slug, (p, sec, tail, intent, note) in KEYWORDS.items():
        o.append("- **`%s`** — %s" % (slug, note))
    o.append("\n### Title and description, as they ship\n")
    o.append(table([("`%s`" % s, pg[s]["title"], len(pg[s]["title"]), len(pg[s]["desc"])) for s in KEYWORDS],
                   ["Page", "Title", "Title chars", "Desc chars"]))
    o.append("\n### Service terms — the 13 rows\n")
    o.append("Each service row and its *Get a quote* link carries its own term, so the hub page can rank for "
             "all thirteen without a page for each.\n")
    o.append(table([(s, "`%s`" % t) for s, t in SERVICE_TERMS.items()], ["Service", "Target term"]))

    o.append("\n## 2. On-page rules\n")
    o.append(table(ONPAGE_RULES, ["Element", "Rule"]))

    o.append("\n## 3. Internal linking\n")
    o.append("The cheapest ranking lever we fully control. Every page links to the quote form; service pages "
             "cross-link to each other so authority circulates instead of pooling on the home page.\n")
    o.append(table([("`%s`" % k, " · ".join("`%s`" % x for x in v)) for k, v in INTERNAL.items()],
                   ["From", "Links to"]))

    o.append("\n## 4. Structured data\n")
    o.append("Hand-written JSON-LD, validated in the Rich Results Test before launch. One `LocalBusiness` "
             "node with an `@id`, referenced by everything else rather than repeated.\n")
    o.append(table(SCHEMA, ["Page", "Types", "Must contain"]))
    o.append("\n```jsonc\n"
             '// the one node everything else points at\n'
             '{\n'
             '  "@context": "https://schema.org",\n'
             '  "@type": "LocalBusiness",\n'
             '  "@id": "https://%s/#business",\n'
             '  "name": "%s",\n'
             '  "url": "https://%s/",\n'
             '  "telephone": "%s",\n'
             '  "email": "info@%s",\n'
             '  "address": { "@type": "PostalAddress", "streetAddress": "ICIPE Road, Sports Drive, Suite 8",\n'
             '               "addressLocality": "Kasarani, Nairobi", "postalCode": "00100",\n'
             '               "addressCountry": "KE" },\n'
             '  "geo": { "@type": "GeoCoordinates", "latitude": "%s", "longitude": "%s" },\n'
             '  "areaServed": [ "Nairobi", "Kiambu" ],\n'
             '  "foundingDate": "2018",\n'
             '  "openingHoursSpecification": [ /* from the client — do not invent hours */ ],\n'
             '  "sameAs": [ /* Facebook, Instagram, LinkedIn — once the handles exist */ ],\n'
             '  "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Cleaning services",\n'
             '                       "itemListElement": [ /* all 13 */ ] }\n'
             '}\n```\n' % (DOMAIN, BRAND, DOMAIN, PHONE_E164, DOMAIN, GEO[0], GEO[1]))

    o.append("\n## 5. Technical foundation\n")
    o.append(table(TECH, ["Item", "What we do"]))

    o.append("\n## 6. Google Business Profile\n")
    o.append("For a service business in Nairobi this outranks the website in importance. Most enquiries will "
             "come through the map pack, not through a blue link.\n")
    o.append(table(GBP, ["Item", "What we do"]))

    o.append("\n## 7. Citations and profiles\n")
    o.append(table(CITATIONS, ["Where", "Why", "When"]))

    o.append("\n## 8. Content that earns rankings\n")
    o.append(table(CONTENT, ["Piece", "Why it wins", "When"]))

    o.append("\n## 9. What will sink this if we let it\n")
    o.append(table(RISKS, ["Risk", "The rule"]))

    o.append("\n## 10. Measurement\n")
    o.append(table(MEASURE, ["When", "What good looks like"]))
    o.append("\n**Honest expectation.** A new domain does not win `cleaning services in Nairobi` quickly. "
             "What it can win inside three months: its own brand name, the local pack around Kasarani and "
             "Ruiru, `post construction cleaning Nairobi`, and the long-tail service terms. That is where "
             "the first jobs come from, and the head term follows the jobs — not the other way round.\n")
    return "\n".join(o) + "\n"


def build():
    md = build_md()
    with open("SEO.md", "w", encoding="utf-8") as f:
        f.write(md)
    n_pages, n_services = len(KEYWORDS), len(SERVICE_TERMS)
    print("SEO verify OK: %d pages mapped, %d service terms, %d internal-link rules, %d schema blocks"
          % (n_pages, n_services, len(INTERNAL), len(SCHEMA)))
    print("wrote SEO.md (%d lines)" % md.count("\n"))


if __name__ == "__main__":
    build()
