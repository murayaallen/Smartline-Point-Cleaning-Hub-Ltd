# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — logo concept presentation.

Four A4 pages: a comparison page, then one card per concept showing the full
lock-up, the mark alone, reversed on navy, one-colour, and the favicon test.
Marks come from logo_concepts.py (SVG) and are rasterised at print resolution.
"""
import io
import os
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

from brandkit import (A4, W, H, M, CW, NAVY, MID, SKY, BODY, MUTE, LINE, SOFT,
                      WHITE, card, draw_para, eyebrow_ls, masthead, footer,
                      tickbox, grad_rule)
from logo_concepts import CONCEPTS, INDIGO, ORANGE, AMBER
from logo_concepts import NAVY as C_NAVY

OUT = "Smartline Point Cleaning Hub - Logo Concepts.pdf"
REF = "AMM-L-2026-187"
DATE = "16/11/2026"
DOMAIN = "smartlinepointcleaning.co.ke"

C_INDIGO = HexColor(INDIGO)
C_ORANGE = HexColor(ORANGE)
CLIENT_NAVY = HexColor(C_NAVY)

_cache = {}


def mark_png(num, name, mode, px=900):
    key = (num, mode, px)
    if key not in _cache:
        f = "logo/svg/%s-%s-%s.svg" % (num, name.lower().replace(" ", "-"), mode)
        doc = pymupdf.open(f)
        pix = doc[0].get_pixmap(dpi=int(px / 100.0 * 72), alpha=True)
        _cache[key] = ImageReader(io.BytesIO(pix.tobytes("png")))
    return _cache[key]


def draw_mark(c, num, name, mode, x, y, size):
    """x, y = bottom-left of the square box"""
    c.drawImage(mark_png(num, name, mode), x, y, size, size, mask="auto")


def wordmark(c, x, y, scale=1.0, dark=CLIENT_NAVY, mid=C_INDIGO, rule=C_ORANGE,
             tagline=True):
    """company name set beside the mark. y = cap height of SMARTLINE."""
    s = scale
    c.setFont("S-B", 18 * s); c.setFillColor(dark)
    cx = x
    for ch in "SMARTLINE":
        c.drawString(cx, y, ch)
        cx += c.stringWidth(ch, "S-B", 18 * s) + 0.6 * s
    c.setFont("S", 7.6 * s); c.setFillColor(mid)
    cx = x + 0.6
    for ch in "POINT CLEANING HUB LTD":
        c.drawString(cx, y - 13 * s, ch)
        cx += c.stringWidth(ch, "S", 7.6 * s) + 1.45 * s
    if tagline:
        c.setFillColor(rule)
        c.rect(x + 1, y - 24 * s, 22 * s, 1.8 * s, stroke=0, fill=1)
        c.setFont("S", 8 * s); c.setFillColor(HexColor("#6B7280"))
        c.drawString(x + 29 * s, y - 26 * s, "Assuring you the best")


def chip(c, x, y, w, h, fill, label, labelcolor=MUTE):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 6, stroke=0, fill=1)
    c.setFont("S", 6.6); c.setFillColor(labelcolor)
    c.drawCentredString(x + w / 2, y - 10, label)


# ================================================================= page 1
def page_overview(c):
    y = masthead(c, "Logo concepts",
                 "Six improved marks for Smartline Point Cleaning Hub Ltd",
                 "%s  ·  %s  ·  new site: %s" % (REF, DATE, DOMAIN))

    sy = y - 24
    rowy = draw_para(
        c,
        "Your current mark already owns three things: the <b>S</b>, the indigo-to-orange "
        "sweep and the droplet. Every concept below keeps all three — none of them asks your "
        "clients to re-learn who you are. What changes is the drawing: even stroke weight, true "
        "arcs, and shapes that hold together on a van door, on an overall, and at the size of a "
        "phone browser tab. Tick the one to take forward, or name two to combine.",
        M, sy, CW, size=9, leading=13.2) - 16

    gw = (CW - 2 * 14) / 3
    gh = 150
    for i, (num, name, fn, note) in enumerate(CONCEPTS):
        x = M + (i % 3) * (gw + 14)
        yy = rowy - (i // 3) * (gh + 16)
        card(c, x, yy - gh, gw, gh, WHITE, LINE, 8, shadow=True)
        draw_mark(c, num, name, "color", x + gw / 2 - 38, yy - 96, 76)
        tickbox(c, x + 14, yy - gh + 14, 12)
        c.setFont("S-SB", 9.6); c.setFillColor(NAVY)
        c.drawString(x + 32, yy - gh + 17, "%s  %s" % (num, name))
    bottom = rowy - 2 * (gh + 16)

    c.setFont("S", 8.4); c.setFillColor(MUTE)
    c.drawString(M, bottom + 2, "Each concept is shown in full on the pages that follow — lock-up, "
                                "reversed, one colour, and at favicon size.")
    footer(c, "Logo concepts  %s" % REF, 1, 4)
    c.showPage()


# ================================================================= cards
def concept_card(c, idx, top_y):
    num, name, fn, note = CONCEPTS[idx]
    ch = 326
    card(c, M, top_y - ch, CW, ch, WHITE, LINE, 9, shadow=True)

    # header strip
    c.setFillColor(SOFT)
    c.roundRect(M, top_y - 40, CW, 40, 9, stroke=0, fill=1)
    c.setFillColor(WHITE); c.rect(M, top_y - 40, CW, 9, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, top_y - 40, W - M, top_y - 40)
    c.setFont("S-L", 20); c.setFillColor(SKY); c.drawString(M + 18, top_y - 28, num)
    c.setFont("S-SB", 13); c.setFillColor(NAVY); c.drawString(M + 48, top_y - 27, name)
    draw_para(c, note, M + 150, top_y - 11, CW - 168, size=8.2, leading=11.2)

    # primary lock-up
    ly = top_y - 62
    eyebrow_ls(c, "PRIMARY LOCK-UP", M + 18, ly, MUTE, 6.6, 1.4)
    draw_mark(c, num, name, "color", M + 18, ly - 86, 74)
    wordmark(c, M + 104, ly - 36, 1.0)

    c.setStrokeColor(LINE); c.setLineWidth(.5)
    c.line(M + 18, ly - 100, W - M - 18, ly - 100)

    # stacked lock-up + mark alone
    sy = ly - 114
    eyebrow_ls(c, "STACKED", M + 18, sy, MUTE, 6.6, 1.4)
    draw_mark(c, num, name, "color", M + 18, sy - 74, 56)
    c.setFont("S-B", 11.5); c.setFillColor(CLIENT_NAVY)
    cx = M + 18
    for chh in "SMARTLINE":
        c.drawString(cx, sy - 88, chh)
        cx += c.stringWidth(chh, "S-B", 11.5) + 0.4
    c.setFont("S", 5.6); c.setFillColor(C_INDIGO)
    cx = M + 18.5
    for chh in "POINT CLEANING HUB LTD":
        c.drawString(cx, sy - 97, chh)
        cx += c.stringWidth(chh, "S", 5.6) + 1.05

    # variants
    vx = M + 150
    eyebrow_ls(c, "REVERSED", vx, sy, MUTE, 6.6, 1.4)
    c.setFillColor(CLIENT_NAVY)
    c.roundRect(vx, sy - 78, 86, 66, 7, stroke=0, fill=1)
    draw_mark(c, num, name, "rev", vx + 13, sy - 71, 52)
    c.setFont("S", 6.6); c.setFillColor(MUTE)
    c.drawString(vx, sy - 90, "uniforms, dark banners")

    mx = vx + 102
    eyebrow_ls(c, "ONE COLOUR", mx, sy, MUTE, 6.6, 1.4)
    c.setFillColor(HexColor("#F1F2F5"))
    c.roundRect(mx, sy - 78, 86, 66, 7, stroke=0, fill=1)
    draw_mark(c, num, name, "mono", mx + 13, sy - 71, 52)
    c.setFont("S", 6.6); c.setFillColor(MUTE)
    c.drawString(mx, sy - 90, "stamps, embroidery")

    fx = mx + 102
    eyebrow_ls(c, "SMALL SIZES", fx, sy, MUTE, 6.6, 1.4)
    c.setStrokeColor(LINE); c.setLineWidth(.6)
    c.roundRect(fx, sy - 78, 86, 66, 7, stroke=1, fill=0)
    draw_mark(c, num, name, "color", fx + 12, sy - 50, 32)
    draw_mark(c, num, name, "color", fx + 52, sy - 42, 16)
    c.setFont("S", 5.6); c.setFillColor(MUTE)
    c.drawString(fx + 14, sy - 60, "32px")
    c.drawString(fx + 54, sy - 60, "16px")
    c.setFont("S", 6.6); c.setFillColor(MUTE)
    c.drawString(fx, sy - 90, "browser tab, avatar")

    # footer strip of the card: where it is used
    uy = sy - 116
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M + 18, uy + 8, W - M - 18, uy + 8)
    tickbox(c, M + 18, uy - 14, 12)
    c.setFont("S-SB", 8.6); c.setFillColor(NAVY)
    c.drawString(M + 38, uy - 11, "Take this one forward")
    return top_y - ch


def page_cards(c, pair, page_no):
    y = H - 46
    from brandkit import logo_mark
    logo_mark(c, M, y - 34, 34)
    c.setFont("S-SB", 11); c.setFillColor(NAVY); c.drawString(M + 44, y - 20, "Allen Muraya Maina")
    c.setFont("S", 8.2); c.setFillColor(MUTE)
    c.drawRightString(W - M, y - 20, "Smartline Point Cleaning Hub Ltd  ·  Logo concepts")
    grad_rule(c, M, y - 44, CW, 2.4)

    ty = y - 70
    for idx in pair:
        ty = concept_card(c, idx, ty) - 22
    footer(c, "Logo concepts  %s" % REF, page_no, 4)
    c.showPage()


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Logo concepts - Smartline Point Cleaning Hub Ltd")
    c.setAuthor("Allen Muraya Maina")
    page_overview(c)
    page_cards(c, (0, 1), 2)
    page_cards(c, (2, 3), 3)
    page_cards(c, (4, 5), 4)
    c.save()
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
