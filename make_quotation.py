# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd - website quotation (issued 16/11/2026).
Figures live in quote_figures.py (verify() on import) and the drawing kit in amm_doc.py,
shared with the final invoice (make_invoice.py). The quotation renders exactly as issued."""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color

from quote_figures import (BUILD, DOMAIN, HOSTING, DEPOSIT_PC, BUILD_DEPOSIT, TOTAL, DUE_NOW, DUE_LIVE,
                           RENEWAL, QUOTE_NO, ksh, verify)
from amm_doc import (NAVY, DEEP, MID, SKY, INDIGO, INK, BODY, MUTE, LINE, SOFT, WHITE, W, H, M, CW,
                     para, draw_para, grad_rule, corner_facets, card, eyebrow_ls, logo_mark)
import amm_doc

DATE  = "16/11/2026"
VALID = "16/12/2026"

OUT = r"d:/Projects/Smartline Point Cleaning Hub Ltd/Smartline Point Cleaning Hub - Website Quotation.pdf"


def footer(c, page):
    amm_doc.footer(c, "Quotation %s" % QUOTE_NO, page, 2)


def payment_schedule(c, sy):
    """payment schedule table; sy = y of the section eyebrow. returns bottom y."""
    eyebrow_ls(c, "PAYMENT SCHEDULE", M, sy, NAVY, 7.4, 1.6)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, sy - 7, W - M, sy - 7)
    tt = sy - 20
    hh = 20
    c.setFillColor(NAVY); c.rect(M, tt - hh, CW, hh, stroke=0, fill=1)
    c.setFillColor(SKY); c.rect(M, tt - hh - 1.6, CW, 1.6, stroke=0, fill=1)
    c.setFont("S-SB", 8.2); c.setFillColor(WHITE)
    c.drawString(M + 12, tt - 14, "STAGE")
    c.drawString(M + 150, tt - 14, "WHEN")
    c.drawRightString(W - M - 12, tt - 14, "AMOUNT (KES)")
    pay = [
        ("Deposit to start", "On acceptance of this quotation",
         "40%% of the build (%s) + domain (%s) + hosting (%s)"
         % (ksh(BUILD_DEPOSIT), ksh(DOMAIN), ksh(HOSTING)), DUE_NOW),
        ("Balance on go-live", "Once the site is live and approved",
         "Remaining 60% of the build", DUE_LIVE),
    ]
    yrow = tt - hh - 1.6
    rh = 34
    for i, (nm, wn, ds, amt) in enumerate(pay):
        if i % 2 == 1:
            c.setFillColor(SOFT); c.rect(M, yrow - rh, CW, rh, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.setLineWidth(.4); c.line(M, yrow - rh, W - M, yrow - rh)
        c.setFont("S-SB", 9.4); c.setFillColor(NAVY); c.drawString(M + 12, yrow - 16, nm)
        c.setFont("S", 8.4); c.setFillColor(BODY); c.drawString(M + 150, yrow - 16, wn)
        c.setFont("S", 7.8); c.setFillColor(MUTE); c.drawString(M + 150, yrow - 27, ds)
        c.setFont("S-SB", 11); c.setFillColor(INK); c.drawRightString(W - M - 12, yrow - 18, ksh(amt))
        yrow -= rh
    c.setFillColor(HexColor("#EEF2F8")); c.rect(M, yrow - 24, CW, 24, stroke=0, fill=1)
    c.setStrokeColor(NAVY); c.setLineWidth(1.0); c.line(M, yrow, W - M, yrow)
    c.setFont("S-SB", 9.6); c.setFillColor(NAVY)
    c.drawString(M + 12, yrow - 16, "TOTAL")
    c.setFont("S-SB", 12); c.drawRightString(W - M - 12, yrow - 17, ksh(TOTAL))
    return yrow - 24


# ================================================================ PAGE 1
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Website Quotation - Smartline Point Cleaning Hub Ltd")
c.setAuthor("Allen Muraya Maina")
c.setSubject("Website, domain and hosting quotation")

corner_facets(c)

top = H - 46
logo_mark(c, M, top - 46, 46)
c.setFont("S-SB", 15); c.setFillColor(NAVY)
c.drawString(M + 58, top - 18, "Allen Muraya Maina")
eyebrow_ls(c, "DESIGN. CODE. EXECUTE.", M + 58, top - 32, MUTE, 7, 1.5)
c.setFont("S", 7.8); c.setFillColor(HexColor("#9AA0AE"))
c.drawString(M + 58, top - 44, "Web Development  \u00b7  Data & Systems Consultant")

rx = W - M
eyebrow_ls(c, "CONTACT", rx - 62, top - 6, HexColor("#A8ACB8"), 6.8, 1.4)
c.setFont("S-SB", 9); c.setFillColor(NAVY); c.drawRightString(rx, top - 20, "+254 792 507 750")
c.setFont("S", 8.4); c.setFillColor(BODY)
c.drawRightString(rx, top - 32, "murayamakingedits@gmail.com")
c.drawRightString(rx, top - 43, "KRA PIN  A013413450I")

grad_rule(c, M, top - 62, CW, 3)

ty = top - 82
c.setFont("S-L", 27); c.setFillColor(NAVY); c.drawString(M, ty - 20, "Quotation")
c.setFont("S-SB", 10.5); c.setFillColor(MID)
c.drawString(M, ty - 38, "Website Design, Build & Launch  \u2014  smartlineltd.co.ke")
c.setFont("S", 8.6); c.setFillColor(MUTE)
c.drawString(M, ty - 51, "Prepared for Smartline Point Cleaning Hub Ltd")

mw, mh = 168, 42
card(c, W - M - mw, ty - 38, mw, mh, SOFT, LINE, 6)
for i, (k, v) in enumerate([("Quote No.", QUOTE_NO), ("Date", DATE)]):
    yy = ty - 10 - i * 15
    c.setFont("S", 8); c.setFillColor(MUTE); c.drawString(W - M - mw + 12, yy, k)
    c.setFont("S-SB", 8.4); c.setFillColor(NAVY); c.drawRightString(W - M - 12, yy, v)

py = ty - 74
ph = 72
pw = CW * 0.555
card(c, M, py - ph, pw, ph, WHITE, LINE, 7)
eyebrow_ls(c, "PREPARED FOR", M + 14, py - 18, SKY, 6.8, 1.5)
c.setFont("S-SB", 10.5); c.setFillColor(NAVY)
c.drawString(M + 14, py - 34, "Smartline Point Cleaning Hub Ltd")
c.setFont("S", 8.3); c.setFillColor(BODY)
c.drawString(M + 14, py - 46, "ICIPE Road, Sports Drive, Suite 8, Kasarani")
c.drawString(M + 14, py - 56, "P.O. Box 48018-00100, Nairobi  \u00b7  +254 711 128736")
c.drawString(M + 14, py - 66, "info@smartlineltd.co.ke")

ox = M + pw + 12
ow = CW - pw - 12
c.saveState()
p = c.beginPath(); p.roundRect(ox, py - ph, ow, ph, 7); c.clipPath(p, stroke=0)
c.linearGradient(ox, py, ox + ow, py - ph, [MID, NAVY, DEEP], [0, .5, 1], extend=True)
c.setFillColor(Color(SKY.red, SKY.green, SKY.blue, alpha=.18))
q = c.beginPath(); q.moveTo(ox + ow, py); q.lineTo(ox + ow, py - 34); q.lineTo(ox + ow - 34, py); q.close()
c.drawPath(q, stroke=0, fill=1)
c.restoreState()
eyebrow_ls(c, "TOTAL INVESTMENT", ox + 14, py - 18, HexColor("#8FC7E8"), 6.8, 1.5)
c.setFont("S", 10); c.setFillColor(HexColor("#B9C4D8")); c.drawString(ox + 14, py - 40, "KES")
c.setFont("S-SB", 23); c.setFillColor(WHITE); c.drawString(ox + 42, py - 42, ksh(TOTAL))
c.setFillColor(SKY); c.rect(ox + 14, py - 54, 22, 1.6, stroke=0, fill=1)
c.setFont("S", 8); c.setFillColor(HexColor("#C8D2E4"))
c.drawString(ox + 14, py - 66, "One-off. Covers year one in full.")

sy = py - ph - 22
eyebrow_ls(c, "WHAT THE BUILD COVERS", M, sy, NAVY, 7.4, 1.6)
c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, sy - 7, W - M, sy - 7)

cards = [
    ("Website build",
     "Hand-coded HTML5, CSS3 and JavaScript — no page-builder, nothing to break. Up to 8 pages."),
    ("Responsive & fast",
     "Built for 320px phones up to wide desktops. WebP images, lazy loading and caching for mobile data."),
    ("Content & company profile",
     "Service copy written for the web, photographs edited, and the company profile redesigned."),
    ("Social media",
     "Launch posts for Facebook, Instagram, LinkedIn and WhatsApp — sized, captioned, ready to publish."),
    ("Google & search",
     "Business Profile verified, Search Console and Analytics, LocalBusiness schema, sitemap and robots.txt."),
    ("Security & handover",
     "SSL auto-renewal, CSP and HSTS headers, clean URLs, spam-protected forms, backups, full handover."),
]
cx0, cy0 = M, sy - 18
cwd = (CW - 2 * 9) / 3
chh = 76
for i, (h1, b1) in enumerate(cards):
    x = cx0 + (i % 3) * (cwd + 9)
    y = cy0 - (i // 3) * (chh + 8)
    card(c, x, y - chh, cwd, chh, WHITE, LINE, 7, shadow=True)
    c.setFillColor(SKY); c.circle(x + 13, y - 16, 2.5, stroke=0, fill=1)
    c.setFont("S-SB", 9.2); c.setFillColor(NAVY); c.drawString(x + 21, y - 19, h1)
    draw_para(c, b1, x + 13, y - 30, cwd - 26, size=7.8, leading=10.9)

ty2 = cy0 - 2 * (chh + 8) - 14
eyebrow_ls(c, "COST BREAKDOWN", M, ty2, NAVY, 7.4, 1.6)
c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, ty2 - 7, W - M, ty2 - 7)

tt = ty2 - 20
hh = 20
c.setFillColor(NAVY); c.rect(M, tt - hh, CW, hh, stroke=0, fill=1)
c.setFillColor(SKY); c.rect(M, tt - hh - 1.6, CW, 1.6, stroke=0, fill=1)
c.setFont("S-SB", 8.2); c.setFillColor(WHITE)
c.drawString(M + 12, tt - 14, "ITEM")
c.drawString(M + 170, tt - 14, "WHAT IT COVERS")
c.drawRightString(W - M - 12, tt - 14, "AMOUNT (KES)")

items = [
    ("Website \u2014 full build", "Code, content, SEO, Google set-up, social posts, company profile, launch", BUILD),
    ("Domain name \u2014 1 year", "smartlineltd.co.ke registered, DNS configured and pointed to the site", DOMAIN),
    ("Server space & email \u2014 1 year", "Hosting, SSL, daily backups and all company email accounts", HOSTING),
]
rh = 24
yrow = tt - hh - 1.6
for i, (nm, ds, amt) in enumerate(items):
    if i % 2 == 1:
        c.setFillColor(SOFT); c.rect(M, yrow - rh, CW, rh, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.setLineWidth(.4); c.line(M, yrow - rh, W - M, yrow - rh)
    c.setFont("S-SB", 9); c.setFillColor(NAVY); c.drawString(M + 12, yrow - 17, nm)
    c.setFont("S", 8.2); c.setFillColor(BODY); c.drawString(M + 170, yrow - 17, ds)
    c.setFont("S-SB", 9.6); c.setFillColor(INK); c.drawRightString(W - M - 12, yrow - 17, ksh(amt))
    yrow -= rh

c.setFillColor(HexColor("#EEF2F8")); c.rect(M, yrow - 24, CW, 24, stroke=0, fill=1)
c.setStrokeColor(NAVY); c.setLineWidth(1.0); c.line(M, yrow, W - M, yrow)
c.setFont("S-SB", 9.6); c.setFillColor(NAVY)
c.drawString(M + 12, yrow - 16, "TOTAL  (inclusive \u2014 no further charges in year one)")
c.setFont("S-SB", 12); c.setFillColor(NAVY); c.drawRightString(W - M - 12, yrow - 17, ksh(TOTAL))

# ---- how it runs (page 1 foot)
sy3 = yrow - 24 - 24
eyebrow_ls(c, "HOW IT RUNS", M, sy3, NAVY, 7.4, 1.6)
c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, sy3 - 7, W - M, sy3 - 7)

steps = [
    ("01", "Deposit", "KES %s paid; domain and hosting bought." % ksh(DUE_NOW)),
    ("02", "Content", "You send logo, photos and service details."),
    ("03", "Build & review", "Built, then shown to you before launch."),
    ("04", "Go-live", "Live and handed over. KES %s due." % ksh(DUE_LIVE)),
]
stx = sy3 - 18
sw = (CW - 3 * 10) / 4
shh = 80
for i, (num, h1, b1) in enumerate(steps):
    x = M + i * (sw + 10)
    card(c, x, stx - shh, sw, shh, WHITE, LINE, 7, shadow=True)
    c.setFillColor(HexColor("#EAF6FD"))
    c.roundRect(x + 13, stx - 26, 21, 15, 4, stroke=0, fill=1)
    c.setFont("S-SB", 8); c.setFillColor(SKY); c.drawCentredString(x + 23.5, stx - 22, num)
    c.setFont("S-SB", 9.4); c.setFillColor(NAVY); c.drawString(x + 13, stx - 42, h1)
    draw_para(c, b1, x + 13, stx - 52, sw - 26, size=7.9, leading=11.2)

footer(c, 1)
c.showPage()

# ================================================================ PAGE 2
corner_facets(c)
top = H - 52
logo_mark(c, M, top - 34, 34)
c.setFont("S-SB", 11); c.setFillColor(NAVY); c.drawString(M + 44, top - 20, "Allen Muraya Maina")
c.setFont("S", 8.2); c.setFillColor(MUTE)
c.drawRightString(W - M, top - 20, "Smartline Point Cleaning Hub Ltd  \u00b7  Website Quotation")
grad_rule(c, M, top - 44, CW, 2.4)

sbot = payment_schedule(c, top - 66)

dy = sbot - 40
dh = 90
c.saveState()
p = c.beginPath(); p.roundRect(M, dy - dh, CW, dh, 8); c.clipPath(p, stroke=0)
c.linearGradient(M, dy, W - M, dy - dh, [MID, NAVY, DEEP], [0, .5, 1], extend=True)
c.setFillColor(Color(SKY.red, SKY.green, SKY.blue, alpha=.16))
q = c.beginPath(); q.moveTo(W - M, dy); q.lineTo(W - M, dy - 46); q.lineTo(W - M - 46, dy); q.close()
c.drawPath(q, stroke=0, fill=1)
c.restoreState()
eyebrow_ls(c, "PAYMENT DETAILS", M + 16, dy - 20, HexColor("#8FC7E8"), 7, 1.5)
c.setFont("S", 8.6); c.setFillColor(HexColor("#C8D2E4"))
c.drawString(M + 16, dy - 38, "M-PESA  \u00b7  Send Money")
c.setFont("S-SB", 19); c.setFillColor(WHITE); c.drawString(M + 16, dy - 62, "0792 507 750")
c.setFont("S", 8.6); c.setFillColor(HexColor("#B9C4D8"))
c.drawString(M + 16, dy - 78, "Registered name:  Allen Muraya Maina")

c.setFont("S", 8.4); c.setFillColor(HexColor("#C8D2E4"))
c.drawRightString(W - M - 16, dy - 38, "KRA PIN   A013413450I")
c.drawRightString(W - M - 16, dy - 52, "Reference:  SMARTLINE")
c.setFont("S-SB", 9); c.setFillColor(WHITE)
c.drawRightString(W - M - 16, dy - 70, "Amount to start:  KES " + ksh(DUE_NOW))
c.setFont("S", 7.8); c.setFillColor(HexColor("#B9C4D8"))
c.drawRightString(W - M - 16, dy - 80, "Forward the M-Pesa message to +254 792 507 750 for your receipt.")

# ---- what the money buys the business
vy = dy - dh - 26
eyebrow_ls(c, "WHAT THIS BUYS THE BUSINESS", M, vy, NAVY, 7.4, 1.6)
c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, vy - 7, W - M, vy - 7)
value = [
    ("Found on Google",
     "Facility managers search before they ask around. A verified profile and a site built to rank "
     "put Smartline in front of them."),
    ("No enquiry lost",
     "Every request lands in info@ with a record and a reply address, instead of a WhatsApp message "
     "that scrolls away by the afternoon."),
    ("Weight in a tender",
     "A company domain, company email and a live profile answer the due-diligence questions buyers "
     "ask before awarding."),
]
vh = 80
vw = (CW - 2 * 9) / 3
for i, (h1, b1) in enumerate(value):
    x = M + i * (vw + 9)
    card(c, x, vy - 18 - vh, vw, vh, SOFT, LINE, 7)
    c.setFillColor(SKY); c.rect(x + 13, vy - 29, 16, 1.8, stroke=0, fill=1)
    c.setFont("S-SB", 9.2); c.setFillColor(NAVY); c.drawString(x + 13, vy - 43, h1)
    draw_para(c, b1, x + 13, vy - 52, vw - 26, size=7.8, leading=10.9)

ny = vy - 18 - vh - 24
eyebrow_ls(c, "TERMS", M, ny, NAVY, 7.4, 1.6)
c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, ny - 7, W - M, ny - 7)
terms = [
    "<b>Timeline.</b> 14\u201321 days from the deposit, once the logo, photographs and service details are received.",
    "<b>Email accounts.</b> info@, accounts@, operations@ and marketing@ are set up as part of the hosting \u2014 "
    "any additional addresses your team needs are added at no extra cost.",
    "<b>Support.</b> Constant and included. Call or message any time after go-live for changes, fixes or advice \u2014 "
    "there is no support window that runs out.",
    "<b>Ownership.</b> The domain, hosting account and website files are registered in the company name and handed over to you.",
    "<b>Renewal from year two.</b> KES %s a year keeps the domain and the server space running. "
    "The build is a one-off charge and does not recur." % ksh(RENEWAL),
]
yy = ny - 18
for t in terms:
    c.setFillColor(SKY); c.circle(M + 3, yy - 4.5, 2.0, stroke=0, fill=1)
    yy = draw_para(c, t, M + 14, yy, CW - 14, size=8.5, leading=12.2, font="S") - 8

# ---- closing line (no signatory block)
c.setFillColor(SKY); c.rect(M, yy - 26, 26, 1.8, stroke=0, fill=1)
c.setFont("S-SB", 9.6); c.setFillColor(NAVY)
c.drawString(M, yy - 44, "Confirm by M-Pesa deposit or a reply to this quotation, and the build starts the same week.")

footer(c, 2)
c.showPage()
c.save()
print("OK ->", OUT)
print("total %s | now %s | on live %s | renewal %s" % (ksh(TOTAL), ksh(DUE_NOW), ksh(DUE_LIVE), ksh(RENEWAL)))
