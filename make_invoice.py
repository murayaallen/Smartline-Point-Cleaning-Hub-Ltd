# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd - final invoice: the balance on go-live, with a full account of
what was delivered. Figures come from quote_figures.py (verify() on import); the look matches the
quotation through amm_doc.py. check() re-reads the rendered PDF and fails loudly on a wrong or
missing figure, a superseded address, or an unembedded font.

    python make_invoice.py
"""
import re
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor

from quote_figures import (BUILD, DOMAIN, HOSTING, BUILD_DEPOSIT, TOTAL, DUE_NOW, DUE_LIVE, RENEWAL,
                           QUOTE_NO, QUOTE_DATE, INVOICE_NO, ksh, verify)
from amm_doc import (NAVY, MID, SKY, INK, BODY, MUTE, LINE, SOFT, WHITE, W, H, M, CW,
                     para, draw_para, card, eyebrow_ls, corner_facets, masthead, running_head, section,
                     navy_panel, footer, KRA_PIN)

INVOICE_DATE = "23/11/2026"
SITE = "smartlinepointcleaning.co.ke"
OUT = r"d:/Projects/Smartline Point Cleaning Hub Ltd/Smartline Point Cleaning Hub - Final Invoice %s.pdf" % INVOICE_NO
PAGES = 3
LABEL = "Invoice %s" % INVOICE_NO

CLIENT = ["Smartline Point Cleaning Hub Ltd", "ICIPE Road, Kasarani, Nairobi",
          "P.O. Box 48018-00100, Nairobi  \u00b7  +254 711 128736", "info@" + SITE]

# ---------------------------------------------------------------- what was delivered (page 2)
DELIVERED = [
    ("The website", [
        "Live at <b>%s</b>: Home, About, Services, Commercial Cleaning, Residential &amp; Apartment "
        "Cleaning, Post-Construction Cleaning, Clients and Contact &mdash; plus a Privacy Notice, a "
        "thank-you page and a branded 404 page." % SITE,
        "Hand-coded HTML5, CSS3 and JavaScript: no page-builder or plug-ins to maintain, and no "
        "monthly platform fee.",
        "Fully responsive &mdash; checked on phones, tablets, laptops and wide screens, 360 to 1920 px.",
    ]),
    ("Brand & design", [
        "The original Smartline logo rebuilt as exact vector artwork from the company profile, sharp "
        "at any size, with files produced for web and print.",
        "Brand colours matched exactly: the indigo S, the navy droplet and the orange swoosh.",
        "Motion with a purpose: a branded loading screen, a squeegee-wipe hero, an interactive "
        "&ldquo;wipe the glass&rdquo; panel and page-to-page transitions &mdash; switched off for "
        "visitors who prefer reduced motion.",
    ]),
    ("Content & photography", [
        "Web copy for all 13 services, the company story, training standards, service areas and "
        "20 answered questions.",
        "The 24-hour re-clean guarantee, and the ten clients served, named with permission.",
        "Over 30 photographs sourced and edited to one bright, people-free look, served in WebP at "
        "three sizes so phones download only what they need.",
    ]),
    ("Enquiries & contact", [
        "A two-step quote form that delivers to info@ and sends the customer an automatic copy.",
        "Spam protection: a hidden trap field, a time check and an hourly limit per visitor.",
        "Call and WhatsApp buttons on every page, a WhatsApp QR code for desktop visitors, and a live "
        "Google map of the office with one-tap directions.",
    ]),
    ("Google & search (SEO)", [
        "Every page has its own search title, description and Nairobi cleaning keywords.",
        "Structured data Google reads directly: business name, address, phone, services and map; "
        "breadcrumbs and FAQs.",
        "XML sitemap and robots.txt; Google Search Console verified and the sitemap submitted; an "
        "instant-indexing key (IndexNow) ready for Bing.",
        "Designed link previews for WhatsApp, Facebook and LinkedIn shares.",
    ]),
    ("Speed & accessibility", [
        "Google Lighthouse at handover: Accessibility 100, Best Practices 100, SEO 100; Performance "
        "96&ndash;97 on phones and 97&ndash;100 on desktop.",
        "Zero layout shift &mdash; nothing jumps while a page loads or scrolls.",
        "Images and the map load only as visitors reach them, saving mobile data.",
    ]),
    ("Security", [
        "SSL certificate (https), with every http and www address redirected to the one secure address.",
        "Strict browser security headers (Content Security Policy, HSTS, clickjacking and content-type "
        "protection); server files blocked from public view; a security.txt contact.",
        "SPF record published, so mail from the company domain is trusted by receiving servers.",
    ]),
    ("Domain, hosting & email", [
        "%s registered for one year and connected to the site." % SITE,
        "Server space and SSL for one year.",
        "Company mailboxes on the domain: info@, accounts@, operations@ and marketing@ &mdash; further "
        "addresses at no extra cost.",
    ]),
    ("Social media launch pack", [
        "46 ready-to-post designs: 9 brand posts, 13 service spotlights, a 6-slide Instagram carousel, "
        "11 Stories / WhatsApp Status designs, 3 link posts, Facebook, LinkedIn and X covers and a "
        "profile picture.",
        "Captions, hashtags and a four-week posting calendar to go with them.",
    ]),
]

CHECKS = [
    ("Live server, 23/11/2026", "https on every address; http, www and .html redirect to the clean address; "
     "real 404 page; server files blocked; sitemap, robots and indexing key served", "All passed"),
    ("Automated browser test", "Every page on phone and desktop: menus, two-step quote form, client "
     "filter, map, loading screens, animations on and off", "All passed"),
    ("Screen widths", "Every page at 360, 768, 1024, 1280 and 1920 px", "No sideways scroll, no errors"),
    ("Layout stability", "Every page, scrolled top to bottom on phone and desktop", "0.000 shift"),
    ("Google Lighthouse", "Phone / desktop, five key pages", "96\u201397 / 97\u2013100 speed \u00b7 100 the rest"),
]

TO_FOLLOW = [
    ("Company profile", "The redesigned company profile carrying the new web address and company "
     "emails &mdash; the current print still shows smartlineltd.co.ke."),
    ("Google Business Profile", "Set up and verified once real photographs of the team at work and the "
     "opening hours are ready &mdash; Google removes stock photos from business profiles."),
    ("Analytics", "Google Analytics switched on whenever visitor figures are wanted, with its consent "
     "notice."),
]

NEXT = [
    "<b>Google indexing.</b> The site is submitted to Google. New websites are crawled and indexed over "
    "the coming weeks, and positions strengthen as the site builds history and visits. Search Console is "
    "watched for anything that needs attention.",
    "<b>Support.</b> Constant and included &mdash; changes, fixes and advice at any time, with no support "
    "window that runs out.",
    "<b>Ownership.</b> The domain, hosting account and website files are registered in the company name.",
    "<b>Renewal.</b> KES %s a year from November 2027 keeps the domain and the server space running. "
    "The build is a one-off charge and does not recur." % ksh(RENEWAL),
]


# ================================================================ PAGE 1 - the invoice
def page_one(c):
    corner_facets(c)
    top = masthead(c)

    ty = top - 82
    c.setFont("S-L", 27); c.setFillColor(NAVY); c.drawString(M, ty - 20, "Invoice")
    c.setFont("S-SB", 10.5); c.setFillColor(MID)
    c.drawString(M, ty - 38, "Website Design, Build & Launch  \u2014  " + SITE)
    c.setFont("S", 8.6); c.setFillColor(MUTE)
    c.drawString(M, ty - 51, "Final invoice  \u00b7  balance on go-live  \u00b7  quotation %s of %s"
                 % (QUOTE_NO, QUOTE_DATE))

    mw, rows = 176, [("Invoice No.", INVOICE_NO), ("Date", INVOICE_DATE), ("Quotation", QUOTE_NO),
                     ("Due", "On receipt")]
    mh = 14 + 15 * len(rows)
    card(c, W - M - mw, ty + 4 - mh, mw, mh, SOFT, LINE, 6)
    for i, (k, v) in enumerate(rows):
        yy = ty - 10 - i * 15
        c.setFont("S", 8); c.setFillColor(MUTE); c.drawString(W - M - mw + 12, yy, k)
        c.setFont("S-SB", 8.4); c.setFillColor(NAVY); c.drawRightString(W - M - 12, yy, v)

    # billed to + balance due
    py, ph, pw = ty - 84, 76, CW * 0.555
    card(c, M, py - ph, pw, ph, WHITE, LINE, 7)
    eyebrow_ls(c, "BILLED TO", M + 14, py - 18, SKY, 6.8, 1.5)
    c.setFont("S-SB", 10.5); c.setFillColor(NAVY); c.drawString(M + 14, py - 34, CLIENT[0])
    c.setFont("S", 8.3); c.setFillColor(BODY)
    for i, ln in enumerate(CLIENT[1:]):
        c.drawString(M + 14, py - 46 - i * 10, ln)
    ox, ow = M + pw + 12, CW - pw - 12
    navy_panel(c, ox, py, ow, ph, r=7, corner=34)
    eyebrow_ls(c, "BALANCE DUE", ox + 14, py - 18, HexColor("#8FC7E8"), 6.8, 1.5)
    c.setFont("S", 10); c.setFillColor(HexColor("#B9C4D8")); c.drawString(ox + 14, py - 41, "KES")
    c.setFont("S-SB", 23); c.setFillColor(WHITE); c.drawString(ox + 42, py - 43, ksh(DUE_LIVE))
    c.setFillColor(SKY); c.rect(ox + 14, py - 55, 22, 1.6, stroke=0, fill=1)
    c.setFont("S", 8); c.setFillColor(HexColor("#C8D2E4"))
    c.drawString(ox + 14, py - 68, "Final payment. The website is live and handed over.")

    # the account
    sy = py - ph - 22
    section(c, "ACCOUNT", sy)
    tt, hh = sy - 20, 20
    c.setFillColor(NAVY); c.rect(M, tt - hh, CW, hh, stroke=0, fill=1)
    c.setFillColor(SKY); c.rect(M, tt - hh - 1.6, CW, 1.6, stroke=0, fill=1)
    c.setFont("S-SB", 8.2); c.setFillColor(WHITE)
    c.drawString(M + 12, tt - 14, "ITEM"); c.drawString(M + 172, tt - 14, "DETAIL")
    c.drawRightString(W - M - 12, tt - 14, "AMOUNT (KES)")
    items = [
        ("Website \u2014 full build", "Design, code, content, SEO, Google set-up, social pack, launch", ksh(BUILD)),
        ("Domain name \u2014 1 year", SITE + " registered and connected to the site", ksh(DOMAIN)),
        ("Server space & email \u2014 1 year", "Hosting, SSL and the company email accounts", ksh(HOSTING)),
    ]
    rh, yrow = 24, tt - hh - 1.6
    for i, (nm, ds, amt) in enumerate(items):
        if i % 2 == 1:
            c.setFillColor(SOFT); c.rect(M, yrow - rh, CW, rh, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.setLineWidth(.4); c.line(M, yrow - rh, W - M, yrow - rh)
        c.setFont("S-SB", 9); c.setFillColor(NAVY); c.drawString(M + 12, yrow - 16, nm)
        c.setFont("S", 8.2); c.setFillColor(BODY); c.drawString(M + 172, yrow - 16, ds)
        c.setFont("S-SB", 9.6); c.setFillColor(INK); c.drawRightString(W - M - 12, yrow - 16, amt)
        yrow -= rh
    # contract total
    c.setStrokeColor(NAVY); c.setLineWidth(.8); c.line(M, yrow, W - M, yrow)
    c.setFont("S-SB", 9); c.setFillColor(NAVY)
    c.drawString(M + 12, yrow - 16, "Contract total")
    c.setFont("S", 8.2); c.setFillColor(BODY)
    c.drawString(M + 172, yrow - 16, "As quoted in %s \u2014 no change to scope or price" % QUOTE_NO)
    c.setFont("S-SB", 9.6); c.setFillColor(INK); c.drawRightString(W - M - 12, yrow - 16, ksh(TOTAL))
    yrow -= rh
    # deposit received
    c.setStrokeColor(LINE); c.setLineWidth(.4); c.line(M, yrow, W - M, yrow)
    c.setFont("S-SB", 9); c.setFillColor(NAVY); c.drawString(M + 12, yrow - 15, "Less: deposit received")
    c.setFont("S", 8.2); c.setFillColor(BODY); c.drawString(M + 172, yrow - 15, "With thanks")
    c.setFont("S", 7.8); c.setFillColor(MUTE)
    c.drawString(M + 172, yrow - 26, "40%% of the build (%s) + domain (%s) + hosting (%s)"
                 % (ksh(BUILD_DEPOSIT), ksh(DOMAIN), ksh(HOSTING)))
    c.setFont("S-SB", 9.6); c.setFillColor(INK); c.drawRightString(W - M - 12, yrow - 17, "\u2212 " + ksh(DUE_NOW))
    yrow -= 34
    # balance due
    c.setFillColor(HexColor("#EEF2F8")); c.rect(M, yrow - 26, CW, 26, stroke=0, fill=1)
    c.setStrokeColor(NAVY); c.setLineWidth(1.0); c.line(M, yrow, W - M, yrow)
    c.setFont("S-SB", 9.8); c.setFillColor(NAVY)
    c.drawString(M + 12, yrow - 17, "BALANCE DUE  \u2014  remaining 60% of the build, on go-live")
    c.setFont("S-SB", 12.5); c.drawRightString(W - M - 12, yrow - 18, "KES " + ksh(DUE_LIVE))
    yrow -= 26

    # at handover
    sy2 = yrow - 24
    section(c, "AT HANDOVER", sy2)
    steps = [
        ("01", "Live", "Online and secure — https on every web address."),
        ("02", "Complete", "8 pages plus privacy, thank-you and 404 pages; all 13 services."),
        ("03", "Tested", "Lighthouse 100 for accessibility, best practices and SEO."),
        ("04", "On Google", "Search Console verified, sitemap submitted."),
    ]
    stx, sw = sy2 - 18, (CW - 3 * 10) / 4
    shh = 50 + max(para(b, size=7.7, leading=10.6).wrap(sw - 24, 1000)[1] for _, _, b in steps) + 12
    for i, (num, h1, b1) in enumerate(steps):
        x = M + i * (sw + 10)
        card(c, x, stx - shh, sw, shh, WHITE, LINE, 7, shadow=True)
        c.setFillColor(HexColor("#EAF6FD")); c.roundRect(x + 13, stx - 26, 21, 15, 4, stroke=0, fill=1)
        c.setFont("S-SB", 8); c.setFillColor(SKY); c.drawCentredString(x + 23.5, stx - 22, num)
        c.setFont("S-SB", 9.4); c.setFillColor(NAVY); c.drawString(x + 13, stx - 41, h1)
        draw_para(c, b1, x + 13, stx - 50, sw - 24, size=7.7, leading=10.6)

    # payment details
    dy, dh = stx - shh - 22, 88
    navy_panel(c, M, dy, CW, dh)
    eyebrow_ls(c, "PAYMENT DETAILS", M + 16, dy - 20, HexColor("#8FC7E8"), 7, 1.5)
    c.setFont("S", 8.6); c.setFillColor(HexColor("#C8D2E4")); c.drawString(M + 16, dy - 38, "M-PESA  \u00b7  Send Money")
    c.setFont("S-SB", 19); c.setFillColor(WHITE); c.drawString(M + 16, dy - 61, "0792 507 750")
    c.setFont("S", 8.6); c.setFillColor(HexColor("#B9C4D8")); c.drawString(M + 16, dy - 77, "Registered name:  Allen Muraya Maina")
    c.setFont("S", 8.4); c.setFillColor(HexColor("#C8D2E4"))
    c.drawRightString(W - M - 16, dy - 38, "KRA PIN   " + KRA_PIN)
    c.drawRightString(W - M - 16, dy - 52, "Reference:  SMARTLINE")
    c.setFont("S-SB", 9.4); c.setFillColor(WHITE)
    c.drawRightString(W - M - 16, dy - 69, "Balance due:  KES " + ksh(DUE_LIVE))
    c.setFont("S", 7.8); c.setFillColor(HexColor("#B9C4D8"))
    c.drawRightString(W - M - 16, dy - 80, "Forward the M-Pesa message to +254 792 507 750 for your receipt.")
    if dy - dh < 66:
        sys.exit("invoice: page 1 overflows into the footer (%.0f)" % (dy - dh))
    footer(c, LABEL, 1, PAGES)


# ================================================================ PAGE 2 - what was delivered
def page_two(c):
    corner_facets(c)
    top = running_head(c, "Smartline Point Cleaning Hub Ltd  \u00b7  Final Invoice")
    sy = top - 66
    section(c, "WHAT HAS BEEN DELIVERED", sy)
    c.setFont("S", 8.3); c.setFillColor(BODY)
    c.drawString(M, sy - 22, "Everything in quotation %s, built, tested and live. In detail:" % QUOTE_NO)

    gap, colw = 8, (CW - 8) / 2
    pad, head_h = 13, 27
    bw = colw - pad * 2 - 10
    fw = CW - pad * 2 - 10

    def body_h(points, width):
        return sum(para(t, size=7.6, leading=10.3).wrap(width, 1000)[1] + 3 for t in points)

    y = sy - 36
    for r in range(0, len(DELIVERED), 2):
        row = DELIVERED[r:r + 2]
        rh = max(head_h + body_h(pts, fw if len(row) == 1 else bw) + 7 for _, pts in row)
        for j, (title, pts) in enumerate(row):
            x = M + j * (colw + gap)
            if len(row) == 1:                      # the last card runs full width
                colw_one = CW
                card(c, x, y - rh, colw_one, rh, WHITE, LINE, 7, shadow=True)
            else:
                card(c, x, y - rh, colw, rh, WHITE, LINE, 7, shadow=True)
            n = r + j + 1
            c.setFillColor(HexColor("#EAF6FD")); c.roundRect(x + pad, y - 22, 19, 13, 3.5, stroke=0, fill=1)
            c.setFont("S-SB", 7.4); c.setFillColor(SKY); c.drawCentredString(x + pad + 9.5, y - 18.6, "%02d" % n)
            c.setFont("S-SB", 9.4); c.setFillColor(NAVY); c.drawString(x + pad + 26, y - 19, title)
            yy = y - head_h
            width = fw if len(row) == 1 else bw
            for t in pts:
                c.setFillColor(SKY); c.circle(x + pad + 2, yy - 4.2, 1.5, stroke=0, fill=1)
                yy = draw_para(c, t, x + pad + 10, yy, width, size=7.6, leading=10.3) - 3
        y -= rh + gap
    if y < 66:
        sys.exit("invoice: page 2 overflows into the footer (%.0f)" % y)
    footer(c, LABEL, 2, PAGES)


# ================================================================ PAGE 3 - checks, to follow, next
def page_three(c):
    corner_facets(c)
    top = running_head(c, "Smartline Point Cleaning Hub Ltd  \u00b7  Final Invoice")
    sy = top - 66
    section(c, "QUALITY CHECKS AT HANDOVER", sy)
    tt, hh = sy - 20, 20
    c.setFillColor(NAVY); c.rect(M, tt - hh, CW, hh, stroke=0, fill=1)
    c.setFillColor(SKY); c.rect(M, tt - hh - 1.6, CW, 1.6, stroke=0, fill=1)
    c.setFont("S-SB", 8.2); c.setFillColor(WHITE)
    c.drawString(M + 12, tt - 14, "CHECK"); c.drawString(M + 128, tt - 14, "WHAT WAS TESTED")
    c.drawRightString(W - M - 12, tt - 14, "RESULT")
    yrow = tt - hh - 1.6
    for i, (nm, what, res) in enumerate(CHECKS):
        p = para(what, size=7.9, leading=10.8)
        _, ph = p.wrap(250, 1000)
        rh = max(26, ph + 14)
        if i % 2 == 1:
            c.setFillColor(SOFT); c.rect(M, yrow - rh, CW, rh, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.setLineWidth(.4); c.line(M, yrow - rh, W - M, yrow - rh)
        c.setFont("S-SB", 8.8); c.setFillColor(NAVY); c.drawString(M + 12, yrow - 16, nm)
        p.drawOn(c, M + 128, yrow - 7 - ph)
        c.setFont("S-SB", 8.6); c.setFillColor(HexColor("#0E7A4B")); c.drawRightString(W - M - 12, yrow - 16, res)
        yrow -= rh

    # included - to follow
    sy2 = yrow - 26
    section(c, "INCLUDED IN THE PRICE \u2014 TO FOLLOW", sy2)
    vw = (CW - 2 * 9) / 3
    vh = 33 + max(para(b, size=7.7, leading=10.6).wrap(vw - 26, 1000)[1] for _, b in TO_FOLLOW) + 13
    for i, (h1, b1) in enumerate(TO_FOLLOW):
        x = M + i * (vw + 9)
        card(c, x, sy2 - 18 - vh, vw, vh, SOFT, LINE, 7)
        c.setFillColor(SKY); c.rect(x + 13, sy2 - 29, 16, 1.8, stroke=0, fill=1)
        c.setFont("S-SB", 9.2); c.setFillColor(NAVY); c.drawString(x + 13, sy2 - 43, h1)
        draw_para(c, b1, x + 13, sy2 - 51, vw - 26, size=7.7, leading=10.6)

    # what happens next
    ny = sy2 - 18 - vh - 26
    section(c, "WHAT HAPPENS NEXT", ny)
    yy = ny - 18
    for t in NEXT:
        c.setFillColor(SKY); c.circle(M + 3, yy - 4.5, 2.0, stroke=0, fill=1)
        yy = draw_para(c, t, M + 14, yy, CW - 14, size=8.4, leading=12.0) - 8

    # closing line
    c.setFillColor(SKY); c.rect(M, yy - 24, 26, 1.8, stroke=0, fill=1)
    c.setFont("S-SB", 9.8); c.setFillColor(NAVY)
    c.drawString(M, yy - 42, "Thank you for choosing us. Payment of KES %s completes the project." % ksh(DUE_LIVE))
    c.setFont("S", 8.4); c.setFillColor(BODY)
    c.drawString(M, yy - 56, "Allen Muraya Maina  \u00b7  Design. Code. Execute.")
    if yy - 56 < 66:
        sys.exit("invoice: page 3 overflows into the footer (%.0f)" % (yy - 56))
    footer(c, LABEL, 3, PAGES)


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Final Invoice %s - Smartline Point Cleaning Hub Ltd" % INVOICE_NO)
    c.setAuthor("Allen Muraya Maina")
    c.setSubject("Website design, build and launch - balance on go-live")
    for fn in (page_one, page_two, page_three):
        fn(c)
        c.showPage()
    c.save()


def check():
    """Re-read the rendered PDF: figures, references, addresses and fonts."""
    import pymupdf
    doc = pymupdf.open(OUT)
    text = "\n".join(p.get_text() for p in doc)
    errs = []
    if len(doc) != PAGES:
        errs.append("%d pages, expected %d" % (len(doc), PAGES))
    for must in (INVOICE_NO, QUOTE_NO, INVOICE_DATE, ksh(BUILD), ksh(DOMAIN), ksh(HOSTING), ksh(TOTAL),
                 ksh(DUE_NOW), ksh(DUE_LIVE), "0792 507 750", KRA_PIN, "SMARTLINE", "info@" + SITE):
        if must not in text:
            errs.append("missing: " + must)
    if text.count("KES " + ksh(DUE_LIVE)) < 3:
        errs.append("balance due should appear on the panel, the table and the payment box")
    if "Sports Drive" in text or "Suite 8" in text:
        errs.append("superseded office address on the invoice")
    if len(re.findall(r"smartlineltd\.co\.ke", text)) != 1:          # only in the company-profile note
        errs.append("old domain smartlineltd.co.ke should appear exactly once (the profile note)")
    # ReportLab's page preamble always declares Helvetica; what matters is that no visible text uses it
    # and that every font the text does use is an embedded subset
    for p in doc:
        embedded = {f[3] for f in p.get_fonts() if f[1] in ("ttf", "cff", "otf") and "+" in f[3]}
        for b in p.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    if sp["text"].strip() and not any(sp["font"] in e or e.endswith(sp["font"]) for e in embedded):
                        errs.append("text set in a non-embedded font: %s (%r)" % (sp["font"], sp["text"][:30]))
    if errs:
        sys.exit("invoice check FAILED:\n  " + "\n  ".join(sorted(set(errs))))
    return len(doc)


if __name__ == "__main__":
    verify()
    build()
    n = check()
    print("OK -> %s (%d pages)" % (OUT, n))
    print("contract %s | deposit received %s | balance due %s" % (ksh(TOTAL), ksh(DUE_NOW), ksh(DUE_LIVE)))
