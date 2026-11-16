# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — premium logo presentation (6 pages A4)."""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor

from logo_premium import (CONCEPTS, INK, INDIGO, BRASS, BRASS_LT, PAPER, STONE,
                          WHITE, GREY, tracked, wordmark, stacked, diamond,
                          mode_colors)
from brandkit import draw_para, logo_mark

W, H = A4
M = 52
CW = W - 2 * M
OUT = "Smartline Point Cleaning Hub - Logo Concepts Rev B.pdf"
REF = "AMM-L-2026-187 / rev B"
DATE = "16/11/2026"
PAGES = 6

MUTED = HexColor("#7A766E")
HAIR = HexColor("#D8D3C8")


def page_bg(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def frame(c, inset=22):
    c.setStrokeColor(HAIR); c.setLineWidth(.6)
    c.rect(inset, inset, W - 2 * inset, H - 2 * inset, stroke=1, fill=0)
    c.setStrokeColor(BRASS); c.setLineWidth(.4)
    c.rect(inset + 4, inset + 4, W - 2 * inset - 8, H - 2 * inset - 8, stroke=1, fill=0)


def head(c, title=None):
    y = H - 62
    logo_mark(c, M, y - 26, 26)
    tracked(c, "ALLEN MURAYA MAINA", M + 36, y - 12, "Copper", 7.4, 1.5, INK)
    tracked(c, "DESIGN. CODE. EXECUTE.", M + 36, y - 22, "Copper", 5.6, 1.2, MUTED)
    if title:
        tracked(c, title, 0, y - 17, "Copper", 7.0, 1.6, MUTED, centre=None)
    tracked(c, "SMARTLINE POINT CLEANING HUB LTD", 0, y - 17, "Copper", 6.6, 1.5,
            MUTED, centre=None) if False else None
    c.setFont("Copper", 6.6); c.setFillColor(MUTED)
    c.drawRightString(W - M, y - 17, "Smartline Point Cleaning Hub Ltd")
    c.setStrokeColor(HAIR); c.setLineWidth(.6)
    c.line(M, y - 38, W - M, y - 38)
    return y - 38


def foot(c, page):
    c.setStrokeColor(HAIR); c.setLineWidth(.6)
    c.line(M, 58, W - M, 58)
    c.setFont("Copper", 6.2); c.setFillColor(MUTED)
    c.drawString(M, 46, "+254 792 507 750")
    c.drawCentredString(W / 2, 46, REF)
    c.drawRightString(W - M, 46, "%d / %d" % (page, PAGES))


def section(c, y, label):
    tracked(c, label, M, y, "Copper", 6.8, 1.6, BRASS)
    c.setStrokeColor(HAIR); c.setLineWidth(.6)
    c.line(M, y - 7, W - M, y - 7)
    return y - 7


# ================================================================= page 1
def cover(c):
    page_bg(c)
    c.setFillColor(INK)
    c.rect(0, H - 232, W, 232, stroke=0, fill=1)
    c.setStrokeColor(BRASS); c.setLineWidth(.6)
    c.line(M, H - 232 + 16, W - M, H - 232 + 16)

    logo_mark(c, M, H - 104, 30)
    tracked(c, "ALLEN MURAYA MAINA", M + 40, H - 94, "Copper", 7.4, 1.5, WHITE)
    c.setFont("Bodoni", 40); c.setFillColor(WHITE)
    c.drawString(M, H - 166, "Logo concepts")
    tracked(c, "SMARTLINE POINT CLEANING HUB LTD", M, H - 190, "Copper", 8.2, 2.2, BRASS_LT)
    c.setFont("Bodoni-I", 10.5); c.setFillColor(HexColor("#B9BCCB"))
    c.drawString(M, H - 210, "Six premium directions  ·  %s  ·  %s" % (REF, DATE))

    y = H - 272
    draw_para(c,
              "Six directions, all built on the same discipline. The letterforms come from a "
              "high-contrast serif rather than drawn shapes, terminals are cut flat, and every rule is "
              "a hairline. The navy is taken deeper than the one on your current profile and the "
              "accent is brass rather than a saturated orange — the combination that reads as a firm "
              "rather than a flyer. Each mark is given room to breathe, so it holds up as a seal on a "
              "tender document and as an embroidered patch on an overall.",
              M, y, CW, size=10, leading=15.2, color=HexColor("#3A3832"))

    # six marks across two rows
    gy = y - 112
    gw = (CW - 2 * 20) / 3
    for i, (num, name, fn, note) in enumerate(CONCEPTS):
        x = M + (i % 3) * (gw + 20)
        yy = gy - (i // 3) * 210
        c.setStrokeColor(HAIR); c.setLineWidth(.6)
        c.rect(x, yy - 150, gw, 150, stroke=1, fill=0)
        fn(c, x + gw / 2 - 48, yy - 118, 96, "color")
        tracked(c, "%s  %s" % (num, name.upper()), 0, yy - 142, "Copper", 7.0, 1.6,
                INK, centre=x + gw / 2)
    foot(c, 1)
    c.showPage()


# ================================================================= page 2
def comparison(c):
    page_bg(c); frame(c)
    y = head(c)
    c.setFont("Bodoni", 23); c.setFillColor(INK)
    c.drawString(M, y - 34, "What each one is for")
    y = y - 58

    rows = [
        ("01", "The Seal", "Tenders, schools, churches, institutional clients",
         "Heaviest to print small; needs 25mm minimum"),
        ("02", "The Plate", "Door signage, folders, foil-blocked cards",
         "Reads as hospitality; less literal about cleaning"),
        ("03", "The Letter", "Everything — the workhorse. Cheapest to apply",
         "Carries no cleaning cue on its own"),
        ("04", "The Cipher", "The most ownable; hotels, apartments, Airbnb hosts",
         "Two letters take a moment longer to read"),
        ("05", "The Droplet", "Keeps the cleaning cue, stays light and modern",
         "Hairline needs care below 15mm"),
        ("06", "The Stamp", "Uniforms, vehicles, anything embroidered or cut",
         "Deliberately quiet; the wordmark does the work"),
    ]
    c.setFont("Copper", 6.6); c.setFillColor(BRASS)
    tracked(c, "MARK", M + 56, y, "Copper", 6.6, 1.5, BRASS)
    tracked(c, "STRONGEST FOR", M + 190, y, "Copper", 6.6, 1.5, BRASS)
    tracked(c, "THE TRADE-OFF", M + 362, y, "Copper", 6.6, 1.5, BRASS)
    c.setStrokeColor(INK); c.setLineWidth(.7); c.line(M, y - 7, W - M, y - 7)
    ry = y - 7
    for i, (num, name, forr, against) in enumerate(rows):
        rh = 54
        if i % 2 == 0:
            c.setFillColor(HexColor("#F2EFE8")); c.rect(M, ry - rh, CW, rh, stroke=0, fill=1)
        CONCEPTS[i][2](c, M + 8, ry - rh + 9, 38, "color")
        tracked(c, "%s  %s" % (num, name.upper()), M + 56, ry - 22, "Copper", 7.6, 1.5, INK)
        draw_para(c, forr, M + 190, ry - 16, 162, size=8.2, leading=11, color=HexColor("#3A3832"))
        draw_para(c, against, M + 362, ry - 16, CW - 362 + M - M - 8, size=8.2,
                  leading=11, color=MUTED)
        c.setStrokeColor(HAIR); c.setLineWidth(.5); c.line(M, ry - rh, W - M, ry - rh)
        ry -= rh

    ry = section(c, ry - 34, "HOW TO CHOOSE")
    draw_para(c,
              "Pick on application, not on the page. Ask where the mark has to live hardest: "
              "<b>on a tender cover</b> → 01 or 02.  <b>On an overall and a van</b> → 03 or 06.  "
              "<b>On Instagram and an apartment noticeboard</b> → 04 or 05. "
              "Say the number, or name two and I will bring one combined version.",
              M, ry - 14, CW, size=9.4, leading=14, color=HexColor("#3A3832"))
    foot(c, 2)
    c.showPage()


# ================================================================= cards
def concept_card(c, idx, top_y):
    num, name, fn, note = CONCEPTS[idx]
    ch = 286
    c.setStrokeColor(HAIR); c.setLineWidth(.6)
    c.rect(M, top_y - ch, CW, ch, stroke=1, fill=0)
    c.setFillColor(INK)
    c.rect(M, top_y - 34, CW, 34, stroke=0, fill=1)
    c.setFont("Bodoni", 16); c.setFillColor(BRASS_LT)
    c.drawString(M + 16, top_y - 23, num)
    tracked(c, name.upper(), M + 44, top_y - 22, "Copper", 9.2, 2.0, WHITE)
    draw_para(c, note, M + 186, top_y - 9, CW - 202, size=8, leading=10.6,
              color=HexColor("#C9CCD8"))

    # primary lock-up
    ly = top_y - 58
    tracked(c, "PRIMARY LOCK-UP", M + 16, ly, "Copper", 6.2, 1.4, MUTED)
    fn(c, M + 16, ly - 92, 80, "color")
    wordmark(c, M + 118, ly - 34, 1.0, "color")

    c.setStrokeColor(HAIR); c.setLineWidth(.5)
    c.line(M + 16, ly - 108, W - M - 16, ly - 108)

    sy = ly - 124
    tracked(c, "STACKED", M + 16, sy, "Copper", 6.2, 1.4, MUTED)
    fn(c, M + 30, sy - 64, 50, "color")
    stacked(c, M + 55, sy - 80, .78, "color")

    vx = M + 150
    tracked(c, "REVERSED", vx, sy, "Copper", 6.2, 1.4, MUTED)
    c.setFillColor(INK); c.rect(vx, sy - 76, 92, 64, stroke=0, fill=1)
    fn(c, vx + 29, sy - 70, 52, "rev")
    c.setFont("S", 6.4); c.setFillColor(MUTED)
    c.drawString(vx, sy - 88, "uniforms, dark banners")

    mx = vx + 108
    tracked(c, "ONE COLOUR", mx, sy, "Copper", 6.2, 1.4, MUTED)
    c.setStrokeColor(HAIR); c.setLineWidth(.5)
    c.rect(mx, sy - 76, 92, 64, stroke=1, fill=0)
    fn(c, mx + 29, sy - 70, 52, "mono")
    c.setFont("S", 6.4); c.setFillColor(MUTED)
    c.drawString(mx, sy - 88, "stamps, embroidery")

    fx = mx + 108
    tracked(c, "SMALL SIZES", fx, sy, "Copper", 6.2, 1.4, MUTED)
    c.setStrokeColor(HAIR); c.setLineWidth(.5)
    c.rect(fx, sy - 76, CW - (fx - M) - 16, 64, stroke=1, fill=0)
    fn(c, fx + 14, sy - 48, 32, "color")
    fn(c, fx + 58, sy - 40, 16, "color")
    c.setFont("S", 5.6); c.setFillColor(MUTED)
    c.drawString(fx + 18, sy - 58, "32px")
    c.drawString(fx + 60, sy - 58, "16px")
    c.setFont("S", 6.4); c.setFillColor(MUTED)
    c.drawString(fx, sy - 88, "browser tab, avatar")

    # choose line
    uy = sy - 108
    c.setStrokeColor(HAIR); c.setLineWidth(.5); c.line(M + 16, uy + 10, W - M - 16, uy + 10)
    c.setStrokeColor(INK); c.setLineWidth(.7)
    c.rect(M + 16, uy - 14, 11, 11, stroke=1, fill=0)
    tracked(c, "TAKE THIS ONE FORWARD", M + 36, uy - 11, "Copper", 7.0, 1.5, INK)
    return top_y - ch


def card_page(c, pair, page_no):
    page_bg(c); frame(c)
    y = head(c)
    ty = y - 22
    for idx in pair:
        ty = concept_card(c, idx, ty) - 26
    foot(c, page_no)
    c.showPage()


# ================================================================= page 6
def applications(c):
    page_bg(c); frame(c)
    y = head(c)
    c.setFont("Bodoni", 23); c.setFillColor(INK)
    c.drawString(M, y - 34, "In use")
    c.setFont("Bodoni-I", 10); c.setFillColor(MUTED)
    c.drawString(M, y - 50, "Shown with 01 The Seal — whichever you pick is built out the same way.")
    mark = CONCEPTS[0][2]

    # business card
    y0 = y - 76
    cw_, chh = 250, 148
    c.setFillColor(WHITE); c.setStrokeColor(HAIR); c.setLineWidth(.6)
    c.rect(M, y0 - chh, cw_, chh, stroke=1, fill=1)
    c.setFillColor(INK); c.rect(M, y0 - chh, cw_, 16, stroke=0, fill=1)
    mark(c, M + 18, y0 - 72, 54, "color")
    wordmark(c, M + 84, y0 - 34, .72, "color", tagline=False)
    c.setFont("S", 6.6); c.setFillColor(HexColor("#3A3832"))
    c.drawString(M + 18, y0 - 96, "MICHAEL  ·  Operations")
    c.drawString(M + 18, y0 - 108, "+254 711 128736")
    c.drawString(M + 18, y0 - 120, "info@smartlinepointcleaning.co.ke")
    tracked(c, "SMARTLINEPOINTCLEANING.CO.KE", M + 18, y0 - chh + 6, "Copper", 5.4, 1.1, BRASS_LT)
    c.setFont("S", 6.4); c.setFillColor(MUTED)
    c.drawString(M, y0 - chh - 12, "Business card, 90 × 54mm")

    # overall patch
    px = M + cw_ + 26
    pw = CW - cw_ - 26
    c.setFillColor(HexColor("#1B2A4A"))
    c.rect(px, y0 - chh, pw, chh, stroke=0, fill=1)
    c.setFillColor(HexColor("#22355C"))
    c.rect(px, y0 - chh, pw, 30, stroke=0, fill=1)
    mark(c, px + pw / 2 - 34, y0 - 92, 68, "rev")
    stacked(c, px + pw / 2, y0 - 108, .72, "rev")
    c.setFont("S", 6.4); c.setFillColor(MUTED)
    c.drawString(px, y0 - chh - 12, "Embroidered on the overall, chest left")

    # van panel
    y1 = y0 - chh - 36
    vh = 150
    c.setFillColor(WHITE); c.setStrokeColor(HAIR); c.setLineWidth(.6)
    c.rect(M, y1 - vh, CW, vh, stroke=1, fill=1)
    c.setFillColor(INK)
    p = c.beginPath()
    p.moveTo(M, y1 - vh); p.lineTo(M + CW, y1 - vh); p.lineTo(M + CW, y1 - vh + 52)
    p.curveTo(M + CW * .60, y1 - vh + 84, M + CW * .34, y1 - vh + 18, M, y1 - vh + 44)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    mark(c, M + 26, y1 - 86, 66, "color")
    wordmark(c, M + 116, y1 - 32, 1.05, "color", tagline=False)
    c.setFont("S", 7.4); c.setFillColor(HexColor("#3A3832"))
    c.drawString(M + 116, y1 - 72, "Commercial  ·  Residential  ·  Post-construction  ·  Deep clean  ·  Landscaping")
    tracked(c, "+254 711 128736", W - M - 172, y1 - 118, "Copper", 9.0, 1.8, WHITE)
    tracked(c, "SMARTLINEPOINTCLEANING.CO.KE", W - M - 172, y1 - 133, "Copper", 6.0, 1.2, BRASS_LT)
    c.setFont("S", 6.4); c.setFillColor(MUTED)
    c.drawString(M, y1 - vh - 12, "Van side panel")

    # next steps
    ny = section(c, y1 - vh - 40, "NEXT")
    draw_para(c,
              "Tell me the number. The chosen mark is then drawn to final vector, with a full file "
              "set — SVG, EPS, PDF, PNG, favicon — plus the one-page rule sheet (clear space, minimum "
              "size, what not to do), and it goes straight onto the website, the company profile, the "
              "signature block and the social launch set.",
              M, ny - 14, CW, size=9.4, leading=14, color=HexColor("#3A3832"))
    foot(c, 6)
    c.showPage()


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Logo concepts - Smartline Point Cleaning Hub Ltd")
    c.setAuthor("Allen Muraya Maina")
    cover(c)
    comparison(c)
    card_page(c, (0, 1), 3)
    card_page(c, (2, 3), 4)
    card_page(c, (4, 5), 5)
    applications(c)
    c.save()
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
