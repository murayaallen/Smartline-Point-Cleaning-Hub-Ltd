# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — one-page choice sheet for the client:
domain name options (checked free on the KENIC register) plus the three other
decisions needed before the build starts."""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from brandkit import (A4, W, H, M, CW, NAVY, DEEP, MID, SKY, INK, BODY, MUTE,
                      LINE, SOFT, WHITE, TINT, card, para, draw_para, eyebrow_ls,
                      masthead, tickbox, footer)

DATE = "16/11/2026"
REF = "AMM-D-2026-187"
OUT = "Smartline Point Cleaning Hub - Domain & Choices.pdf"

# domain options: (name, note, recommended)
DOMAINS = [
    ("smartlineltd.co.ke",
     "Matches the domain and the email already printed in your company profile, and the registered "
     "company name. Nothing you have already given out goes out of date.", True),
    ("smartlinecleaning.co.ke",
     "Puts the service in the name, which helps a little when someone searches for cleaning in Nairobi. "
     "Your current profile would need reprinting.", False),
    ("smartlinecleaners.co.ke",
     "Same idea, phrased around the team rather than the service.", False),
    ("smartlinepoint.co.ke",
     "Shorter, carries the Point in your name, says nothing about what you do.", False),
    ("smartlinehub.co.ke",
     "Shorter, carries the Hub in your name, says nothing about what you do.", False),
    ("smartlinepointcleaning.co.ke",
     "Closest to the full company name, but long to say on a call and long to print.", False),
]

CHOICES = [
    ("Naming your clients on the website",
     ["Yes — publish the full list from your profile (Jewel Complex, Uwezo Microfinance Bank, Richland Pointe and the rest)",
      "No — describe the work without naming the clients",
      "Publish only the ones I tick on the list"]),
    ("Prices on the website",
     ["Show starting prices or ranges per service",
      "No prices — every job quoted after a site visit"]),
    ("WhatsApp button on the site",
     ["Use +254 711 128736 (the number on your profile)",
      "Use a different number: ____________________"]),
]


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Domain name options and build choices - Smartline Point Cleaning Hub Ltd")
    c.setAuthor("Allen Muraya Maina")

    y = masthead(c, "Your choices",
                 "Domain name, and three decisions before the build starts",
                 "Smartline Point Cleaning Hub Ltd  ·  %s  ·  %s" % (REF, DATE))

    # ---- domain section
    sy = y - 20
    eyebrow_ls(c, "1.  CHOOSE YOUR DOMAIN NAME", M, sy, NAVY, 7.4, 1.6)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, sy - 7, W - M, sy - 7)

    rowy = draw_para(c, "Every name below was checked on the Kenyan domain register on %s and is free. "
                        "Tick one and send this sheet back — it is registered the same day, and your "
                        "email addresses follow it: info@, accounts@, operations@, marketing@." % DATE,
                     M, sy - 18, CW, size=8.5, leading=11.8) - 10

    for name, note, rec in DOMAINS:
        nw = CW - 36 - (118 if rec else 24)
        _, nh = para(note, size=7.9, leading=10.6).wrap(nw, 1000)
        rh = 26 + nh
        card(c, M, rowy - rh, CW, rh, TINT if rec else WHITE, SKY if rec else LINE, 7,
             lw=1.0 if rec else .6, shadow=rec)
        tickbox(c, M + 14, rowy - 24, 12)
        c.setFont("S-SB", 11); c.setFillColor(NAVY)
        c.drawString(M + 36, rowy - 22, name)
        if rec:
            chip_w = 96
            c.setFillColor(SKY)
            c.roundRect(W - M - chip_w - 13, rowy - 25, chip_w, 15, 4, stroke=0, fill=1)
            c.setFont("S-SB", 6.8); c.setFillColor(WHITE)
            c.drawCentredString(W - M - 13 - chip_w / 2, rowy - 20.5, "OUR RECOMMENDATION")
        draw_para(c, note, M + 36, rowy - 26, nw, size=7.9, leading=10.6)
        rowy -= rh + 5

    rowy = draw_para(c, "smartline.co.ke is not on this list — another company registered it in April 2026, "
                        "so it cannot be used.", M + 2, rowy - 4, CW - 4, size=8, leading=10.8, color=MUTE)

    # ---- other decisions
    sy2 = rowy - 20
    eyebrow_ls(c, "2.  THREE MORE DECISIONS", M, sy2, NAVY, 7.4, 1.6)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, sy2 - 7, W - M, sy2 - 7)

    by = sy2 - 22
    for title, opts in CHOICES:
        c.setFillColor(SKY); c.circle(M + 3, by - 3, 2.2, stroke=0, fill=1)
        c.setFont("S-SB", 9.4); c.setFillColor(NAVY)
        c.drawString(M + 13, by - 6, title)
        oy = by - 18
        for o in opts:
            tickbox(c, M + 15, oy - 8, 10)
            end = draw_para(c, o, M + 32, oy, CW - 46, size=8.3, leading=11.4)
            oy = end - 5
        by = oy - 6

    footer(c, "Domain & choices  %s" % REF)
    c.showPage()
    c.save()
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
